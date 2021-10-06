import helpers

STOCK_DATA = {
    "farm": ["Cereals", "CRL", 0],
    "mine": ["Chocolate", "CHC", 1],
    "factory": ["Butter", "BTR", 2],
    "bank": ["Sugar", "SUG", 3],
    "temple": ["Nuts", "NUT", 4],
    "wizard tower": ["Salt", "SLT", 5],
    "shipment": ["Vanilla", "VNL", 6],
    "alchemy lab": ["Eggs", "EGG", 7],
    "portal": ["Cinnamon", "CNM", 8],
    "time machine": ["Cream", "CRM", 9],
    "antimatter condenser": ["Jam", "JAM", 10],
    "prism": ["White Chocolate", "WCH", 11],
    "chancemaker": ["Honey", "HNY", 12],
    "fractal engine": ["Cookies", "CKI", 13],
    "javascript console": ["Recipes", "RCP", 14],
    "idleverse": ["Subsidiaries", "SBD", 15]
}


class StockMode:
    # 0: stable - 12.5% chance: -5% delta, -0.025 - 0.025 delta fluctuation
    # 1: slow rise - 25% chance: -1% delta, -0.005 - 0.005 delta fluct.
    # 2: slow fall - 25% chance: -1% delta, -0.045 - 0.005 delta fluct.
    # 3: fast rise - 12.5% chance: stock value fluct. between 0 - 1, -0.015 - 0.135 delta fluct.,
    # 30% value fluct between -7 and 3
    # 4: fast fall - 12.5% chance: stock value fluct. between -1 - 0, -0.135 - 0.015 delta fluct.,
    # 30% value fluct between -3 and 7
    # 5: chaotic - 12.5% chance: 50% chance stock value fluct. between -5 - 5, -0.15 - 0.15 delta fluct.,
    # 30% value fluct between -3 and 7

    STABLE = 0
    SLOW_RISE = 1
    SLOW_FALL = 2
    FAST_RISE = 3
    FAST_FALL = 4
    CHAOTIC = 5


class Stock:
    def __init__(self, office_level: int, bank_level: int, src_building_name: str, src_building_quantity: int,
                 src_building_level: int, duration: int, value: float, mode: int, delta: float, held: int):
        st = STOCK_DATA[src_building_name.lower()]
        self.id: int = st[2]
        """The ID of this stock, from 0-14."""

        self.name: str = st[0]
        """The name of the stock."""

        self.symbol: str = st[1]
        """The three-letter symbol of the stock."""

        self.duration: int = duration
        """The remaining duration of the current mode. Ticks down every minute."""

        self.value: float = value
        """The current value of the stock, measured in $econds of CPS. Ex. $1200 = 20 minutes of CPS."""

        self.mode: int = mode
        """The mode the stock is currently in."""

        self.delta: float = delta
        """The amount randomly added to the value."""

        self.held: int = held
        """The amount of this stock currently in possession."""

        self.resting_value: int = 10 * (self.id + 1) + (bank_level - 1)
        """The value that the stock tends to go towards. Increases with the level of banks."""

        self.capacity: int = src_building_level * 10
        """The amount of this stock that can be held. Depends on the building associated with the stock."""

        if office_level > 0:
            self.capacity += 25
        if office_level > 1:
            self.capacity += 50
        if office_level > 2:
            self.capacity += 75
        if office_level > 3:
            self.capacity += 100

        if office_level > 4:
            self.capacity += src_building_quantity * 1.5
        else:
            self.capacity += src_building_quantity

        ###################
        # Bot specific attributes
        ###################

        self.boughtFor: float = 0.0
        """The amount of cookies paid for this stock in this cycle.
        Zero indicates the bot has not purchased this stock yet. Includes overhead."""

        self.soldFor: float = 0.0
        """The amount of cookies gained from this stock in this cycle."""

        self.lifetimeEarnings: float = 0.0
        """The net profit of this stock."""

    def __str__(self):
        modes = ["stable", "slow rise", "slow fall", "fast rise", "fast fall", "chaotic"]
        return f"{self.symbol} ~ Valued at ${self.value:.2f} | {self.held}/{self.capacity} held | {self.duration}min " \
               f"remaining in {modes[self.mode]} mode | {self.getRestingDiff():.2f}% from resting"

    def getRestingDiff(self) -> float:
        """
        Get the percentage of the current value over the resting value.

        :return: The float containing the result.
        :rtype: float
        """
        return round(((self.value / self.resting_value) - 1) * 100, 2)

