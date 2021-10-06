import logging
import math
import os
import time
from typing import List, Dict

import pyautogui
import toml

import helpers
from building import Building
from config import Config
from smarket.stock import Stock, STOCK_DATA, StockMode


class Market:
    """
    The class that contains functions to manage the stock market minigame.
    """

    def __init__(self, config: Config, saveData: str, buildings: Dict[str, Building]):
        data = saveData.split(" ")
        gen = data[0].split(":")
        self.logger = logging.getLogger("wafer")
        self.filename = "smarket/mdata.toml"
        self.bank_level = buildings["bank"].level

        self.officeLevel: int = int(gen[0])
        """The current office level. Used to buy loans (unimplemented) or to influence storage capacity."""
        self.brokers: int = int(gen[1])
        """The current amount of brokers. Each reduces overhead by 5% (multiplicative)."""

        stockSaves = data[1].split("!")
        self.config = config
        self.stocks: List[Stock] = self.loadStocks(stockSaves, buildings)

    def loadStocks(self, stockSaves: List[str], buildings: Dict[str, Building]):
        """
        Load stock objects from a string representation.

        :param stockSaves: The data associated with the market minigame.
        :param buildings: Information on the buildings currently owned.
        :return: A list of the generated stock objects.
        """
        stocks = []
        index = 0
        self.bank_level = buildings["bank"].level
        for key, value in STOCK_DATA.items():
            if value[2] == index:
                save = stockSaves[index].split(":")
                bdata = buildings[key.lower()]
                stocks.append(Stock(
                    office_level=self.officeLevel,
                    bank_level=self.bank_level,
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
        return stocks

    def updateStocks(self, stockSaves: List[str], buildings: Dict[str, Building]):
        """
        Update the class stock list with a fresh stock list.

        :param stockSaves: The data associated with the market minigame.
        :param buildings: Information on the buildings currently owned.
        """
        newStocks = self.loadStocks(stockSaves, buildings)
        for count, stock in enumerate(self.stocks):
            newStocks[count].boughtFor = stock.boughtFor
            newStocks[count].lifetimeEarnings = stock.lifetimeEarnings
            newStocks[count].soldFor = stock.soldFor
        self.stocks = newStocks

    def getStock(self, symbol: str = "", index: int = -1) -> Stock:
        """
        Get stock by index or symbol.

        :param symbol: The symbol of the stock.
        :param index: The ID of the stock.
        :return: The stock object associated with the attributes.
        """
        if symbol:
            for s in self.stocks:
                if s.symbol == symbol:
                    return s
        elif index != -1:
            for s in self.stocks:
                if s.id == index:
                    return s

    def getStockPrice(self, stock: Stock, quantity: int) -> float:
        """
        Get the value of this stock for X quantity of items. Measured in seconds of the highest
        CPS in this ascension.

        :param stock: The stock to get the value of.
        :param quantity: The quantity of this stock being purchased.
        :return: The adjusted value of the stock.
        """
        value = stock.value * quantity
        return round(value + (value * 0.2 * math.pow(0.95, self.brokers)), 2)

    def getStockBuyPriceRaw(self, stock: Stock, quantity: int) -> float:
        """
        Get the amount of cookies required to buy this stock.

        :param stock: The stock being purchased.
        :param quantity: The amount of stock being bought.
        :return: The amount of cookies required to buy the stock.
        """
        ascCPS = helpers.getHighestAscensionCPS(self.config)
        overhead = 1 + (0.2 * math.pow(0.95, self.brokers))
        return ascCPS * stock.value * overhead * quantity

    def getStockSalePriceRaw(self, stock: Stock, quantity: int) -> float:
        """
        Get the amount of cookies gained from selling a stock.

        :param stock: The stock that is being sold.
        :param quantity: The amount of stock that is being sold.
        :return: The cookies gained from selling this stock.
        """
        ascCPS = helpers.getHighestAscensionCPS(self.config)
        return ascCPS * stock.value * quantity

    def getAmountCanPurchase(self, stock: Stock) -> int:
        """
        Get the maximum amount of a stock that can be bought with the current amount of cookies.
        Capped at the stock's capacity.

        :param stock: The stock to compare to.
        :return: The amount of this stock that can be bought.
        """
        amount = 1
        cookies = helpers.getCookies(self.config)
        while self.getStockBuyPriceRaw(stock, amount) < cookies:
            amount += 1
        if amount > stock.capacity:
            amount = stock.capacity
        return amount

    def evaluateStocks(self) -> int:
        """
        Decide what stocks should be bought or sold, depending on the configuration.

        Each stock mode has its own behavior. If a stock surpasses the market cap of
        $100 + $3(Bank level-1), then it is automatically sold.

        A return value of 0 means no changes happened, negative numbers mean more stocks were
        sold than bought, and positive numbers mean more stocks were bought than sold.

        :returns: The changes made this tick.
        """
        buy_list: List[Stock] = []
        sell_list: List[Stock] = []
        for stock in self.stocks:
            diff = stock.getRestingDiff()
            mode = stock.mode
            dur = stock.duration
            surpassedCap = stock.value >= 100 + (3*(self.bank_level-1))
            if diff <= self.config.buyLimit and stock.held == 0:
                if mode == StockMode.STABLE and dur <= 30:
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
            elif (diff >= self.config.sellLimit or surpassedCap) and stock.held > 0:
                if surpassedCap:
                    # it is going to start decreasing immediately after this
                    sell_list.append(stock)
                elif mode == StockMode.STABLE or mode == StockMode.CHAOTIC \
                        or mode == StockMode.FAST_FALL or mode == StockMode.SLOW_FALL:
                    sell_list.append(stock)
                # in fast-rise mode there's a 3% chance every tick of it changing to fast fall
                # at >=400 ticks there's >11% chance of that happening so at that point just sell
                elif mode == StockMode.FAST_RISE and (dur >= 400 or dur <= 5):
                    sell_list.append(stock)
                elif mode == StockMode.SLOW_RISE and dur <= 5:
                    sell_list.append(stock)
        for stock in buy_list:
            self.logger.info(f"Buying {self.getAmountCanPurchase(stock)} of {stock.symbol} at ${stock.value:.2f} "
                             f"({stock.getRestingDiff():.2f}% from resting)")
            amountBuying = self.getAmountCanPurchase(stock)
            self.buyStock(stock)
            self.recordPurchase(stock, amountBuying, self.getStockBuyPriceRaw(stock, amountBuying))
            stock.held = amountBuying
        for stock in sell_list:
            self.logger.info(f"Selling {stock.held} of {stock.symbol} at ${stock.value:.2f} "
                             f"({stock.getRestingDiff():.2f}% from resting)")
            salePrice = self.getStockSalePriceRaw(stock, stock.held)
            self.sellStock(stock)
            self.recordSale(stock, salePrice)
            stock.held = 0
        return len(buy_list) - len(sell_list)

    def buyStock(self, stock: Stock):
        """
        Click the "max buy" button to buy the maximum amount of stock possible.

        :param stock: The stock to purchase.
        """
        point = helpers.locateAll("img/buyStockButton.png")[stock.id]
        pyautogui.click(point)

    def sellStock(self, stock: Stock):
        """
        Click the "max sell" button to sell all current stock held.

        :param stock: The stock to sell.
        """
        point = helpers.locateAll("img/sellStockButton.png")[stock.id]
        pyautogui.click(point)

    def _loadRecordFile(self):
        data = {}

        with open(self.filename, "r" if os.path.exists(self.filename) else "a+") as f:
            try:
                data = toml.load(f)

                # try accessing variables
                data["inventory"]
                data["sold"]
            except (toml.TomlDecodeError, TypeError, KeyError):
                self.logger.info("Creating purchase record.")
        if not data:
            data = {
                "inventory": {},
                "sold": {}
            }
        return data

    def recordPurchase(self, stock: Stock, quantity: int, purchaseAmount: float):
        """
        Save the information about the current stock purchase to the save file.
        Used to keep track of profit margins.

        :param stock: The stock that was purchased.
        :param quantity: The amount of stock that was purchased.
        :param purchaseAmount: The amount of cookies spent to purchase this item.
        """
        data = self._loadRecordFile()

        data["inventory"][str(int(time.time()))+f"-{stock.symbol}"] = {
            "amount": quantity,
            "purchasedFor": purchaseAmount,
            "symbol": stock.symbol,
            "value": stock.value,
        }
        stock.boughtFor = purchaseAmount

        with open(self.filename, "w") as f:
            toml.dump(data, f)

    def recordSale(self, stock: Stock, salePrice: float):
        """
        Record the cookies made from selling a stock, and remove them from the bot's inventory.
        Used to keep track of profits.

        :param stock: The stock that was sold.
        :param salePrice: The amount of cookies gained from selling this stock.
        """
        data = self._loadRecordFile()

        ref = ""
        for k, v in data["inventory"].items():
            if stock.symbol in k:
                ref = k

        identifier = str(int(time.time())) + f"-{stock.symbol}"
        data["sold"][identifier] = {
            "amount": stock.held,
            "soldFor": salePrice,
            "soldValue": stock.value,
            "symbol": stock.symbol,
        }
        if ref:
            data["sold"][identifier]["boughtFor"] = data["inventory"][ref]["purchasedFor"]
            data["sold"][identifier]["boughtValue"] = data["inventory"][ref]["value"]

        # take it out of the dictionary to avoid duplicates.
        data["inventory"].pop(ref, None)
        with open(self.filename, "w") as f:
            toml.dump(data, f)
