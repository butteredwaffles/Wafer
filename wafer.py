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
    """
    The main app class. Links all "modules" together and handles initialization.
    """
    GOLD_COOKIE_COLOR_1 = (193, 155, 71)
    GOLD_COOKIE_COLOR_2 = (225, 201, 111)

    gardenEnabled: bool
    mainAutoClickerEnabled: bool
    goldenCookieAutoClickerEnabled: bool

    def __init__(self, gardenEnabled: bool = True,
                 mainAutoClickerEnabled: bool = True,
                 goldenCookieAuto: bool = True):
        """
        Initialize the Wafer class with any configuration options.

        :param gardenEnabled: Enables/disables the auto-play of the "farm" minigame.
        :param mainAutoClickerEnabled: Enables/disables auto-clicking the big cookie.
        :param goldenCookieAuto: Enables/disables auto-clicking any golden cookie that appears.
        """
        self.cookieCoords = None
        self.logger = logging.getLogger("wafer")
        self._lock = threading.Lock()
        self.running = True
        self.mainClickingPaused = False

        self.gardenData = None
        self.loadSave()

        self.gardenEnabled = gardenEnabled
        self.mainAutoClickerEnabled = mainAutoClickerEnabled
        self.goldenCookieAutoClickerEnabled = goldenCookieAuto

    def run(self) -> None:
        """
        Start the bot.

        :rtype: None
        """
        with ThreadPoolExecutor(max_workers=3) as executor:
            # The main auto clicker has its own thread to avoid constant interruption by
            # other bot actions. Other tasks, such as golden cookie clicking, happen infrequently
            # enough to run in one thread.
            if self.mainAutoClickerEnabled:
                executor.submit(self.clickMainCookie)
            executor.submit(self.runTasks)

    def findGoldenCookies(self) -> List[pyautogui.Point]:
        """
        Search the screen for golden cookies and log their coordinates.

        :return: A list of `pyautogui.Point` objects corresponding to the coordinates of the golden cookies on-screen.
        :rtype: list
        """
        coords: List[pyautogui.Point] = []
        sc = pyautogui.screenshot()
        # Must search using color instead of by image because golden cookies rotate, bounce around,
        # etc. while also sharing the texture with the large normal cookie leading to confusion.
        for x in range(200, sc.width - 200, 2):
            for y in range(200, sc.height - 200, 2):
                pixel = sc.getpixel((x, y))
                if pixel == self.GOLD_COOKIE_COLOR_1 or pixel == self.GOLD_COOKIE_COLOR_2:
                    self.logger.info(f"Located golden cookie at ({x}, {y}).")
                    coords.append(pyautogui.Point(x=x, y=y))
        return coords

    def clickMainCookie(self) -> None:
        """
        Click the large cookie on the left of the screen.

        Will run in an infinite loop, but will exit if the failsafe is detected.

        :rtype: None
        """
        self.logger.info("Locating main cookie...")
        for i in range(20):
            self.cookieCoords = pyautogui.locateOnScreen("img/mainCookie.png", grayscale=True, confidence=0.5)
            if self.cookieCoords:
                self.logger.info("Found main cookie.")
                break
        if not self.cookieCoords:
            self.logger.critical("Could not locate main cookie.")
            self.mainAutoClickerEnabled = False
        else:
            self.logger.info("Beginning main cookie autoclicker.")

        while self.running and self.mainAutoClickerEnabled:
            try:
                while not self.mainClickingPaused:
                    pyautogui.click(self.cookieCoords)
            except pyautogui.FailSafeException:
                self.logger.critical("Detected failsafe. Stopping.")
                self.running = False

    def loadSave(self) -> None:
        """
        Read the user's save file and assign the appropriate values to class variables.

        :rtype: None
        """
        # Currently only worrying about garden data - add on as more
        # features implemented
        with open(_SAVE_LOCATION, "rb") as file:
            # Data has a lot of extra information at the end for some reason after the %.
            data = file.read().split(b"%")[0]
            missing_padding = len(data) % 4
            if missing_padding:
                data += b'=' * (4 - missing_padding)
            data = str(base64.urlsafe_b64decode(data)).split('|')
            farmBuildingData = data[5].split(';')[2]
            gardenData = farmBuildingData.split(",")[4]
            self.gardenData = gardenData

    def runTasks(self) -> None:
        """
        Decide which features of the bot are enabled and activate the corresponding functions.

        This function also handles the interval at which each task will be run.\n
        - Golden cookies are searched for every second.\n
        - Farm is currently managed every minute, but in the future may change depending on soil.\n
        Will run in an infinite loop, but will exit if failsafe is detected.

        :rtype: None
        """
        # TODO: Change tend time based on soil type
        # TODO: Grab farm level from save file.
        nextTend = datetime.now()
        nextGoldenCookieSearch = datetime.now()

        try:
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
                            self.loadSave()
                        nextTend += timedelta(minutes=1)
                        farmLevel = 5
                        farm = Garden(self.gardenData, farmLevel)
                        with self._lock:
                            self.mainClickingPaused = True
                            self.tendGarden(farm)
                            self.mainClickingPaused = False
        except pyautogui.FailSafeException:
            self.logger.critical("Detected failsafe. Stopping.")
            self.running = False

    def tendGarden(self, farm: Garden) -> None:
        """
        Manage events occuring inside of the garden minigame.

        Harvest all plants with <= 3 ticks left to live.

        :param farm: The `Garden` object that represents the current state of the garden.
        :type farm: Garden
        :rtype: None
        """
        # TODO: Add ability to plant crops.
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
                    self.logger.info(
                        f"Harvesting plot of {plot.data.name} located at ({plot.x}, {plot.y}) due to near-death.")
                    pyautogui.click(coord)
                    time.sleep(0.5)
                self._closeGarden()
        except pyautogui.FailSafeException:
            return  # handled in the runTasks function anyway since another function would have caught it as well
        except Exception as e:
            self.logger.exception(e)

    def _closeGarden(self) -> bool:
        """
        Helper function to close the garden window.

        Exists because leaving the window open is just asking for a golden cookie to spawn on top of a crop
        and accidentally cause the bot to harvest it.

        :return: True if garden was closed successfully, False otherwise.
        :rtype: bool
        """
        for i in range(20):
            if self.running:
                coords = pyautogui.locateOnScreen("img/closeGarden.png", grayscale=True, confidence=0.9)
                if coords:
                    pyautogui.click(coords)
                    return True
        return False

    def _openGarden(self) -> bool:
        """
        Helper function to open the garden window.

        :return: True if garden was opened successfully, False otherwise.
        :rtype: bool
        """
        for i in range(20):
            if self.running:
                coords = pyautogui.locateOnScreen("img/viewGarden.png", grayscale=True, confidence=0.8)
                if coords:
                    pyautogui.click(coords)
                    return True
        return False
