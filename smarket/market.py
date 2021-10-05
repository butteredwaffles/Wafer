from typing import List, Dict

from building import Building
from smarket import stock


class Market:
    def __init__(self, saveData: str, buildings: Dict[str, Building]):
        data = saveData.split(" ")
        gen = data[0].split(":")

        # TODO: Take office level into account for capacity
        self.officeLevel: int = int(gen[0])
        """The current office level. Used to buy loans (unimplemented) or to influence storage capacity."""
        self.brokers: int = int(gen[1])
        """The current amount of brokers. Each reduces overhead by 5%."""
        self.stocks: List[stock.Stock] = []

        stockSaves = data[1].split("!")
        self.loadStocks(stockSaves, buildings)

    def loadStocks(self, stockSaves: List[str], buildings: Dict[str, Building]):
        self.stocks = []
        index = 0
        bank_level = buildings["bank"].level
        for key, value in stock.STOCK_DATA.items():
            if value[2] == index:
                save = stockSaves[index].split(":")
                bdata = buildings[key.lower()]
                self.stocks.append(stock.Stock(
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
