

class PlantData:
    # All plants grow from 0-100. ageTick controls the increments
    name: str
    id: int
    unlocked: bool
    mutations: list[int]
    children: list[int]
    cost: int  # Measured in minutes of CPS
    minAgeTick: float = 0.0
    maxAgeTick: float = 0.0
    mature: int  # determines how fast things mature, lower numbers = faster maturation
    immortal: bool
    fungus: bool
    weed: bool
    plantable: bool
