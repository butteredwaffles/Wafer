from dataclasses import dataclass


@dataclass
class PlantData:
    # All plants grow from 0-100. ageTick controls the increments
    unlocked: bool
    mutations: list[int]
    cost: int  # Measured in minutes of CPS
    minAgeTick: float
    maxAgeTick: float
    mature: int  # determines how fast things mature, lower numbers = faster maturation
