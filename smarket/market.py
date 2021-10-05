import logging
import math
from typing import List, Dict

import helpers
from building import Building
from config import Config
from smarket.stock import Stock, STOCK_DATA, StockMode


class Market:
    def __init__(self, config: Config, saveData: str, buildings: Dict[str, Building]):
        data = saveData.split(" ")
        gen = data[0].split(":")
        self.logger = logging.getLogger("wafer")

        # TODO: Take office level into account for capacity
        self.officeLevel: int = int(gen[0])
        """The current office level. Used to buy loans (unimplemented) or to influence storage capacity."""
        self.brokers: int = int(gen[1])
        """The current amount of brokers. Each reduces overhead by 5%."""
        self.stocks: List[Stock] = []

        stockSaves = data[1].split("!")
        self.config = config
        self.loadStocks(stockSaves, buildings)

    def loadStocks(self, stockSaves: List[str], buildings: Dict[str, Building]):
        self.stocks = []
        index = 0
        bank_level = buildings["bank"].level
        for key, value in STOCK_DATA.items():
            if value[2] == index:
                save = stockSaves[index].split(":")
                bdata = buildings[key.lower()]
                self.stocks.append(Stock(
                    bank_level=bank_level,
                    src_building_name=bdata.name.lower(),
                    src_building_quantity=bdata.amount,
                    src_building_level=bdata.level,
                    value=float(save[0]) / 100,
                    mode=int(save[1]),
                    delta=float(save[2]),
                    duration=int(save[3]),
                    held=int(save[4])
                ))
                index += 1

    def getStock(self, symbol: str = "", index: int = -1):
        if symbol:
            for s in self.stocks:
                if s.symbol == symbol:
                    return s
        elif index != -1:
            for s in self.stocks:
                if s.id == index:
                    return s

    def getStockPrice(self, stock: Stock, quantity: int) -> float:
        value = stock.value * quantity
        return round(value + (value * 0.2 * math.pow(0.95, self.brokers)), 2)

    def getStockPriceRaw(self, stock: Stock, quantity: int) -> float:
        ascCPS = helpers.getHighestAscensionCPS(self.config)
        overhead = 1 + (0.2 * math.pow(0.95, self.brokers))
        return ascCPS * stock.value * overhead * quantity

    def getAmountCanPurchase(self, stock: Stock):
        amount = 1
        cookies = helpers.getCookies(self.config)
        while self.getStockPriceRaw(stock, amount) < cookies:
            amount += 1
        if amount > stock.capacity:
            amount = stock.capacity
        return amount

    def evaluateStocks(self):
        buy_list: List[Stock] = []
        sell_list: List[Stock] = []
        for stock in self.stocks:
            diff = stock.getRestingDiff()
            mode = stock.mode
            dur = stock.duration
            if diff <= self.config.buyLimit:
                if mode == StockMode.STABLE and dur <= 50:
                    # stable is probably not going much of anywhere so buy now?
                    buy_list.append(stock)
                elif mode == StockMode.CHAOTIC:
                    # no telling what it's going to do
                    buy_list.append(stock)
                elif mode == StockMode.SLOW_FALL and dur <= 5:
                    # safe to wait
                    buy_list.append(stock)
                elif mode == StockMode.SLOW_RISE or mode == StockMode.FAST_RISE:
                    # get now before price rises more
                    buy_list.append(stock)
                elif mode == StockMode.FAST_FALL and dur <= 5:
                    # safe to wait (mostly)
                    buy_list.append(stock)
            elif diff >= self.config.sellLimit:
                if mode == StockMode.STABLE or mode == StockMode.CHAOTIC \
                        or mode == StockMode.FAST_FALL or mode == StockMode.SLOW_FALL:
                    sell_list.append(stock)
                # in fast-rise mode there's a 3% chance every tick of it changing to fast fall
                # at 400 ticks there's about an 11% chance of that happening so at that point just sell
                elif mode == StockMode.FAST_RISE and (dur >= 400 or dur <= 5):
                    sell_list.append(stock)
                elif mode == StockMode.SLOW_RISE and dur <= 5:
                    sell_list.append(stock)
        for stock in buy_list:
            self.logger.info(f"Buying {self.getAmountCanPurchase(stock)} of {stock.symbol} at ${stock.value:.2f} "
                             f"({stock.getRestingDiff():.2f}% from resting)")
        for stock in sell_list:
            self.logger.info(f"Selling {stock.held} of {stock.symbol} at ${stock.value:.2f} "
                             f"({stock.getRestingDiff():.2f}% from resting)")

