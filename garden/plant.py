from dataclasses import dataclass
from . import PlantData
import math


@dataclass
class Plant:
    data: PlantData
    ticksUntilDecay: int
    ticksUntilMature: int

    def __init__(self, lifeTick: int):
        # ignore plot modifiers for now
        self.ticksUntilMature = math.ceil(
            (100/(self.data.minAgeTick+self.data.maxAgeTick/2))
            * ((self.data.mature - lifeTick) / 100)
        )
        self.ticksUntilDecay = math.ceil(
            (100 / (self.data.minAgeTick + self.data.maxAgeTick / 2))
            * ((100 - lifeTick) / 100)
        )