from dataclasses import dataclass
from datetime import datetime
from .plantData import PlantData
from .plant import Plant
import csv
import re

_CSV_FILENAME = "garden/cookieClickerPlants.csv"
# Index is the farm level minus one.
# Format is x1, y1, x2, y2
_PLOT_LIMITS = [
    [2, 2, 4, 4],
    [2, 2, 5, 4],
    [2, 2, 5, 5],
    [1, 2, 5, 5],
    [1, 1, 5, 5],
    [1, 1, 6, 5],
    [1, 1, 6, 6],
    [0, 1, 6, 6],
    [0, 0, 6, 6],
]

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
    plots: list[Plant]
    farmLevel: int

    # Garden information starts before the first colon.
    def __init__(self, dataString: str, farmLevel: int):
        data = re.split(r'[\s:]', dataString)
        self.farmLevel = farmLevel
        self.nextStep = datetime.fromtimestamp(float(data[0]) / 1000)
        self.soil = int(data[1])
        self.nextSoil = datetime.fromtimestamp(float(data[2]) / 1000)
        self.frozen = int(data[3]) == 1
        self.matureHarvests = int(data[4])
        self.totalHarvests = int(data[5])
        # data[6] is irrelevant - just asks if the garden window is open
        self.timesSacrificed = int(data[7])
        # data[8] is also unneeded - seems to be related to freezing?
        self.loadAllPlantData(data[10])
        self.loadAllPlotData(':'.join(data[11:len(data)]))

    def loadAllPlantData(self, unlockedStr: str):
        index = 0
        self.unlockedPlants = []
        with open(_CSV_FILENAME, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data = PlantData()
                data.unlocked = unlockedStr[index] == "1"
                data.name = row["Name"]
                data.id = int(row["ID"])
                data.cost = int(row["Cost"])
                data.minAgeTick = float(row["AgeTick"])
                data.maxAgeTick = float(row["AgeTickR"])
                data.mature = int(row["Mature"])
                data.children = [int(plantID) for plantID in row["Children"].split('|') if row["Children"]]
                data.immortal = row["Immortal"] == "yes"
                data.fungus = row["Fungus"] == "yes"
                data.weed = row["Weed"] == "yes"
                data.plantable = row["Plantable"] == "yes"
                self.unlockedPlants.append(data)

    def loadAllPlotData(self, plotStr: str):
        p = plotStr.split(':')
        p.pop()
        p = iter(p)
        self.plots = []
        index = 0
        limits = _PLOT_LIMITS[self.farmLevel-1]
        for plantID in p:
            life = next(p)
            if int(plantID) > 0:
                plantInfo = self.unlockedPlants[int(plantID)-1]
                plant = Plant(plantInfo, int(life))

                plant.x = int(index%6) - limits[0]
                plant.y = int(index/6) - limits[1]
                self.plots.append(plant)
            index += 1