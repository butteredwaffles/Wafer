from datetime import datetime
from .plantData import PlantData
from .plant import Plant
from typing import Optional
import csv
import re
import pyautogui

_CSV_FILENAME = "garden/cookieClickerPlants.csv"

# The size of the garden is a 6x6 grid, but it will be smaller if your farm level is < 10.
# This array holds information for the size reduction. Index is the farm level minus one.
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


class Garden:
    """
    Class representing the Garden minigame unlocked when you use a sugar lump to level up the Farm.
    """
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
        """
        Initialize a garden object.

        :param dataString: The save information for the garden, resembling XX:XXXX:XXXXX:XXXX 1001010 XXX
        :param farmLevel: The level of the farm.
        :type dataString: str
        :type farmLevel: int
        """
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

        self.farmPlotCoords = None

    def getPlotCoords(self, plant: Plant) -> Optional[pyautogui.Point]:
        """
        Take a Plant object as input and locate its position on the game screen.

        :param plant: A Plant object containing the information for the plot you are looking for.
        :return: The coordinates in a pyautogui.Point object, or None if not found.
        :rtype: pyautogui.Point
        """
        #  This is necessary since hovered tooltips can block the identification.
        pyautogui.moveTo(x=30, y=30)
        if not self.farmPlotCoords:
            for i in range(10):
                farmPlotCoords = pyautogui.locateCenterOnScreen("img/gardenPlot.png", grayscale=True, confidence=0.8)

                if farmPlotCoords:
                    self.farmPlotCoords = farmPlotCoords
                    break
            # farmPlotCoords holds location of [0, 0] plot
        if self.farmPlotCoords:
            point = pyautogui.Point(self.farmPlotCoords.x + (60*plant.x), self.farmPlotCoords.y + (60*plant.y))
            return point
        return None

    def loadAllPlantData(self, unlockedStr: str) -> None:
        """
        Load information for all plants from a .csv file and store it in a class variable.

        :param unlockedStr: A series of 0s and 1s corresponding to each plant's unlocked status.
        :type unlockedStr: str
        :rtype: None
        """
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
                data.ageTick = float(row["AgeTick"])
                data.ageTickR = float(row["AgeTickR"])
                data.mature = int(row["Mature"])
                data.children = [int(plantID) for plantID in row["Children"].split('|') if row["Children"]]
                data.immortal = row["Immortal"] == "yes"
                data.fungus = row["Fungus"] == "yes"
                data.weed = row["Weed"] == "yes"
                data.plantable = row["Plantable"] == "yes"
                self.unlockedPlants.append(data)

    def loadAllPlotData(self, plotStr: str) -> None:
        """
        Create a grid of plants based on save data and store it in a class variable.

        :param plotStr: The string consisting of the plant data and growth stage for every grid space.
        :rtype: None
        """
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
