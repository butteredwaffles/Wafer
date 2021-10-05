import math


class Building:
    """
    Parent class representing a building in game.

    Buildings, unlike Plants, are seperated into individual classes for possible
    building-specific features down the line.
    """
    name: str = 0
    id: int = 0
    amount: int = 0
    bought: int = 0
    totalCookiesProduced: int = 0
    level: int = 0
    highestAmountOwned: int = 0
    _baseCost: int = 0

    def __init__(self, name: str, id: int, amount: int, bought: int, totalCookies: int, level: int, highest: int):
        """
        Initialize a Building object. This constructor is only used directly by children classes.

        :param name: The name of the building.
        :param id: The index/id of the building.
        :param amount: The amount of this building owned.
        :param bought: The amount of this building bought by the player.
        :param totalCookies: The amount of cookies this building has produced.
        :param level: The level of this building.
        :param highest: The highest amount of this building that has been owned.
        """
        self.name = name
        self.id = id
        self.amount = amount
        self.bought = bought
        self.totalCookiesProduced = totalCookies
        self.level = level
        self.highest = highest

    def getCost(self) -> int:
        """
        Get the amount of cookies necessary to purchase another building of this type.
        Formula is base price * 1.15^(amount owned - free buildings), rounded up.

        :return: The cost for the next building.
        :rtype: int
        """
        return self._baseCost * math.ceil(math.pow(1.15, (self.amount - (self.amount - self.bought))))

    def __repr__(self):
        return f"{self.name} Lv.{self.level}: x{self.amount} | {self.totalCookiesProduced} cookies spawned"


"""
All the building types are below.
"""


class Cursors(Building):
    def __init__(self, amount: int, bought: int, total: int, level: int, highest: int):
        super(Cursors, self).__init__("Cursor", 0, amount, bought, total, level, highest)
        self._baseCost = 15


class Grandmas(Building):
    def __init__(self, amount: int, bought: int, total: int, level: int, highest: int):
        super(Grandmas, self).__init__("Grandma", 1, amount, bought, total, level, highest)
        self._baseCost = 100


class Farms(Building):
    def __init__(self, amount: int, bought: int, total: int, level: int, highest: int):
        super(Farms, self).__init__("Farm", 2, amount, bought, total, level, highest)
        self._baseCost = 1100


class Mines(Building):
    def __init__(self, amount: int, bought: int, total: int, level: int, highest: int):
        super(Mines, self).__init__("Mine", 3, amount, bought, total, level, highest)
        self._baseCost = 12000


class Factories(Building):
    def __init__(self, amount: int, bought: int, total: int, level: int, highest: int):
        super(Factories, self).__init__("Factory", 4, amount, bought, total, level, highest)
        self._baseCost = 130000


class Banks(Building):
    def __init__(self, amount: int, bought: int, total: int, level: int, highest: int):
        super(Banks, self).__init__("Bank", 5, amount, bought, total, level, highest)
        self._baseCost = 1400000


class Temples(Building):
    def __init__(self, amount: int, bought: int, total: int, level: int, highest: int):
        super(Temples, self).__init__("Temple", 6, amount, bought, total, level, highest)
        self._baseCost = 20000000


class WizardTowers(Building):
    def __init__(self, amount: int, bought: int, total: int, level: int, highest: int):
        super(WizardTowers, self).__init__("Wizard Tower", 7, amount, bought, total, level, highest)
        self._baseCost = 330000000


class Shipments(Building):
    def __init__(self, amount: int, bought: int, total: int, level: int, highest: int):
        super(Shipments, self).__init__("Shipment", 8, amount, bought, total, level, highest)
        self._baseCost = 5100000000


class AlchemyLabs(Building):
    def __init__(self, amount: int, bought: int, total: int, level: int, highest: int):
        super(AlchemyLabs, self).__init__("Alchemy Lab", 9, amount, bought, total, level, highest)
        self._baseCost = 75000000000


class Portals(Building):
    def __init__(self, amount: int, bought: int, total: int, level: int, highest: int):
        super(Portals, self).__init__("Portal", 9, amount, bought, total, level, highest)
        self._baseCost = 1000000000000


class TimeMachines(Building):
    def __init__(self, amount: int, bought: int, total: int, level: int, highest: int):
        super(TimeMachines, self).__init__("Time Machine", 10, amount, bought, total, level, highest)
        self._baseCost = 14000000000000


class Condensers(Building):
    def __init__(self, amount: int, bought: int, total: int, level: int, highest: int):
        super(Condensers, self).__init__("Antimatter Condenser", 11, amount, bought, total, level, highest)
        self._baseCost = 170000000000000


class Prisms(Building):
    def __init__(self, amount: int, bought: int, total: int, level: int, highest: int):
        super(Prisms, self).__init__("Prism", 12, amount, bought, total, level, highest)
        self._baseCost = 2100000000000000


class Chancemakers(Building):
    def __init__(self, amount: int, bought: int, total: int, level: int, highest: int):
        super(Chancemakers, self).__init__("Chancemaker", 13, amount, bought, total, level, highest)
        self._baseCost = 26000000000000000


class FractalEngines(Building):
    def __init__(self, amount: int, bought: int, total: int, level: int, highest: int):
        super(FractalEngines, self).__init__("Fractal Engine", 14, amount, bought, total, level, highest)
        self._baseCost = 310000000000000000


class Consoles(Building):
    def __init__(self, amount: int, bought: int, total: int, level: int, highest: int):
        super(Consoles, self).__init__("Javascript Console", 15, amount, bought, total, level, highest)
        self._baseCost = 71000000000000000000


class Idleverses(Building):
    def __init__(self, amount: int, bought: int, total: int, level: int, highest: int):
        super(Idleverses, self).__init__("Idleverse", 16, amount, bought, total, level, highest)
        self._baseCost = 12000000000000000000000


BUILDING_TYPES = [Cursors, Grandmas, Farms, Mines, Factories, Banks, Temples, WizardTowers, Shipments,
                  AlchemyLabs, Portals, TimeMachines, Condensers, Prisms, Chancemakers, FractalEngines,
                  Consoles, Idleverses]
