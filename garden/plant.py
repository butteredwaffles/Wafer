from dataclasses import dataclass
from .plantData import PlantData
import math


class Plant:
    data: PlantData = None
    ticksUntilDecay: int = 0
    ticksUntilMature: int = 0
    isMature: bool = False
    x: int = 0
    y: int = 0

    def __init__(self, data_: PlantData, lifeTick: int):
        # ignore plot modifiers for now
        self.data = data_
        self.isMature = self.data.mature <= lifeTick

        if self.isMature:
            self.ticksUntilDecay = math.ceil(
                (100 / (self.data.minAgeTick + self.data.maxAgeTick / 2))
                * ((100 - lifeTick) / 100)
            )
        else:
            self.ticksUntilMature = math.ceil(
                (100 / (self.data.minAgeTick + self.data.maxAgeTick / 2))
                * ((self.data.mature - lifeTick) / 100)
            )

    def __repr__(self):
        if self.isMature:
            maturity = f"Decays in {self.ticksUntilDecay} ticks"
        else:
            maturity = f"Matures in {self.ticksUntilMature} ticks"
        return f"{self.data.name} ({self.x}, {self.y}) {maturity}"