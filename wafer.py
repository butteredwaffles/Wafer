import pyautogui
import threading
import base64
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

from garden.garden import Garden

_GARDEN_SAVE_TEST = "1632097684929:0:1632004711938:1:224:228:1:0:1630975793383: 1111000010000000000000000000000000 0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:1:45:0:0:2:72:0:0:0:0:0:0:0:0:4:43:0:0:0:0:0:0:0:0:5:35:0:0:3:30:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:,0,101"
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
        self._lock = threading.Lock()
        self.running = True
        self.mainClickingPaused = False

        self.gardenData = None
        self.getSave()

        self.gardenEnabled = gardenEnabled
        self.mainAutoClickerEnabled = mainAutoClickerEnabled
        self.goldenCookieAutoClickerEnabled = goldenCookieAuto

    def run(self):
        self.calibrate()
        with ThreadPoolExecutor(max_workers=3) as executor:
            if self.mainAutoClickerEnabled:
                executor.submit(self.clickMainCookie)
            executor.submit(self.runTasks)

    def clickGoldenCookies(self):
        print("Beginning search for golden cookies.")
        sc = pyautogui.screenshot()
        for x in range(200, sc.width - 200, 2):
            for y in range(200, sc.height - 200, 2):
                pixel = sc.getpixel((x, y))
                if pixel == self.GOLD_COOKIE_COLOR_1 or pixel == self.GOLD_COOKIE_COLOR_2:
                    print(f"Located golden cookie at ({x}, {y}). Clicking...")
                    with self._lock:
                        self.mainClickingPaused = True
                        pyautogui.click(x=x, y=y)
                        self.mainClickingPaused = False
                    return True
        print("No golden cookie found.")
        return False

    def clickMainCookie(self):
        print("Clicking main cookie.")
        while self.running:
            try:
                while not self.mainClickingPaused:
                    pyautogui.click(self.cookieCoords)
            except pyautogui.FailSafeException:
                print("Detected failsafe. Exiting.")
                self.running = False

    def calibrate(self):
        print("Locating main cookie...")
        for i in range(100):
            self.cookieCoords = pyautogui.locateOnScreen("img/mainCookie.png", grayscale=True, confidence=0.5)
            if self.cookieCoords:
                print("Found main cookie.\n")
                break
        if not self.cookieCoords:
            print("Could not locate main cookie.")

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
                    self.clickGoldenCookies()
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
                        coord = farm.getPlotCoords(plot)
                        if coord:
                            coords.append([plot, coord])
            if len(coords) > 0:
                self._openGarden()
                for c_data in coords:
                    plot = c_data[0]
                    coord = c_data[1]
                    print(f"Harvesting plot of {plot.data.name} located at ({plot.x}, {plot.y}) due to near-death.")
                    pyautogui.click(coord)
                    time.sleep(0.5)
                self._closeGarden()
        except Exception as e:
            print(e)

    def _closeGarden(self):
        for i in range(20):
            if self.running:
                coords = pyautogui.locateOnScreen("img/closeGarden.png", grayscale=True, confidence=0.8)
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
