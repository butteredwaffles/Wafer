from dataclasses import dataclass
from datetime import datetime
from . import PlantData
from . import Plant

# 100,100,9162377854,5,1632091959972:0:1632004711938:0:219:223:1:0:1630975793383: 1110000010000000000000000000000000 0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:2:0:0:0:0:0:0:0:1:33:4:51:2:72:0:0:0:0:0:0:0:0:0:0:3:13:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:,0,100
@dataclass
class Garden:
    nextStep: datetime
    soil: int
    nextSoil: datetime
    frozen: bool
    matureHarvests: int
    totalHarvests: int
    timesSacrificed: int
    unlockedPlants: list[PlantData]
    plants: list[Plant]
