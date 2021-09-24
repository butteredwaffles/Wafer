from typing import List

import pyautogui
import threading
import base64
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

from garden.garden import Garden

_SAVE_LOCATION = r"C:\Program Files (x86)\Steam\steamapps\common\Cookie Clicker\resources\app\save\save.cki"

class Wafer:
    GOLD_COOKIE_COLOR_1 = (193, 155, 71)
    GOLD_COOKIE_COLOR_2 = (225, 201, 111)

    gardenEnabled: bool
    mainAutoClickerEnabled: bool
    goldenCookieAutoClickerEnabled: bool

    def __init__(self, gardenEnabled: bool = True,
                 mainAutoClickerEnabled: bool = True,
                 goldenCookieAuto: bool = True):
        self.cookieCoords = None
        self.logger = logging.getLogger("wafer")
        self._lock = threading.Lock()
        self.running = True
        self.mainClickingPaused = False

        self.gardenData = None
        self.getSave()

        self.gardenEnabled = gardenEnabled
        self.mainAutoClickerEnabled = mainAutoClickerEnabled
        self.goldenCookieAutoClickerEnabled = goldenCookieAuto

    def run(self):
        with ThreadPoolExecutor(max_workers=3) as executor:
            if self.mainAutoClickerEnabled:
                executor.submit(self.clickMainCookie)
            executor.submit(self.runTasks)

    def findGoldenCookies(self):
        coords: List[pyautogui.Point] = []
        sc = pyautogui.screenshot()
        for x in range(200, sc.width - 200, 2):
            for y in range(200, sc.height - 200, 2):
                pixel = sc.getpixel((x, y))
                if pixel == self.GOLD_COOKIE_COLOR_1 or pixel == self.GOLD_COOKIE_COLOR_2:
                    self.logger.info(f"Located golden cookie at ({x}, {y}).")
                    coords.append(pyautogui.Point(x=x, y=y))
        return coords

    def clickMainCookie(self):
        self.logger.info("Locating main cookie...")
        for i in range(20):
            self.cookieCoords = pyautogui.locateOnScreen("img/mainCookie.png", grayscale=True, confidence=0.5)
            if self.cookieCoords:
                self.logger.info("Found main cookie.")
                break
        if not self.cookieCoords:
            self.logger.critical("Could not locate main cookie.")
        self.logger.info("Beginning main cookie autoclicker.")
        while self.running:
            try:
                while not self.mainClickingPaused:
                    pyautogui.click(self.cookieCoords)
            except pyautogui.FailSafeException:
                self.logger.critical("Detected failsafe. Exiting.")
                self.running = False

    def getSave(self):
        # Currently only worrying about garden data - add on as more
        # features implemented
        with open(_SAVE_LOCATION, "rb") as file:
            data = file.read().split(b"%")[0]
            missing_padding = len(data) % 4
            if missing_padding:
                data += b'=' * (4 - missing_padding)
            data = str(base64.urlsafe_b64decode(data)).split('|')
            farmBuildingData = data[5].split(';')[2]
            gardenData = farmBuildingData.split(",")[4]
            self.gardenData = gardenData

    def runTasks(self):
        nextTend = datetime.now()
        nextGoldenCookieSearch = datetime.now()

        while self.running:
            if self.goldenCookieAutoClickerEnabled:
                if nextGoldenCookieSearch <= datetime.now():
                    gCookies = self.findGoldenCookies()
                    if len(gCookies) > 0:
                        with self._lock:
                            self.mainClickingPaused = True
                            for gCookie in gCookies:
                                pyautogui.click(gCookie)
                                time.sleep(0.3)
                            self.mainClickingPaused = False
                    nextGoldenCookieSearch += timedelta(seconds=1)
            if self.gardenEnabled:
                if nextTend <= datetime.now():
                    with self._lock:
                        self.getSave()
                    # TODO: Change tend time based on soil type
                    nextTend += timedelta(minutes=1)
                    farmLevel = 5  # TODO: Grab from save file.
                    farm = Garden(self.gardenData, farmLevel)
                    with self._lock:
                        self.mainClickingPaused = True
                        self.tendGarden(farm)
                        self.mainClickingPaused = False

    def tendGarden(self, farm):
        try:
            coords = []
            for plot in farm.plots:
                if plot.isMature:
                    if plot.ticksUntilDecay <= 3:
                        if not farm.farmPlotCoords:
                            self._openGarden()
                            coord = farm.getPlotCoords(plot)
                            self._closeGarden()
                        else:
                            coord = farm.getPlotCoords(plot)
                        if coord:
                            coords.append([plot, coord])
            if len(coords) > 0:
                self._openGarden()
                for c_data in coords:
                    plot = c_data[0]
                    coord = c_data[1]
                    self.logger.info(f"Harvesting plot of {plot.data.name} located at ({plot.x}, {plot.y}) due to near-death.")
                    pyautogui.click(coord)
                    time.sleep(0.5)
                self._closeGarden()
        except Exception as e:
            self.logger.exception(e)

    def _closeGarden(self):
        for i in range(20):
            if self.running:
                coords = pyautogui.locateOnScreen("img/closeGarden.png", grayscale=True, confidence=0.9)
                if coords:
                    pyautogui.click(coords)
                    return True
        return False

    def _openGarden(self):
        for i in range(20):
            if self.running:
                coords = pyautogui.locateOnScreen("img/viewGarden.png", grayscale=True, confidence=0.8)
                if coords:
                    pyautogui.click(coords)
                    return True
        return False
