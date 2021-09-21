import pyautogui
import threading
import time
from concurrent.futures import ThreadPoolExecutor

from garden.garden import Garden

_GARDEN_SAVE_TEST = "1632097684929:0:1632004711938:1:224:228:1:0:1630975793383: 1111000010000000000000000000000000 0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:1:45:0:0:2:72:0:0:0:0:0:0:0:0:4:43:0:0:0:0:0:0:0:0:5:35:0:0:3:30:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:,0,101"


class Wafer:
    GOLD_COOKIE_SEARCH_TIMER = 0.0  # in seconds
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

        self.gardenEnabled = gardenEnabled
        self.mainAutoClickerEnabled = mainAutoClickerEnabled
        self.goldenCookieAutoClickerEnabled = goldenCookieAuto

    def run(self):
        self.calibrate()
        with ThreadPoolExecutor(max_workers=3) as executor:
            if self.mainAutoClickerEnabled:
                executor.submit(self.clickMainCookie)
            if self.goldenCookieAutoClickerEnabled:
                executor.submit(self.clickGoldenCookies)
            executor.submit(self.runTasks)

    def clickGoldenCookies(self):
        print("Beginning search for golden cookies.")
        while self.running:
            sc = pyautogui.screenshot()
            for x in range(300, sc.width - 300):
                for y in range(300, sc.height - 300):
                    pixel = sc.getpixel((x, y))
                    if pixel == self.GOLD_COOKIE_COLOR_1 or pixel == self.GOLD_COOKIE_COLOR_2:
                        print(f"Located golden cookie at ({x}, {y}). Clicking...")
                        with self._lock:
                            self.mainClickingPaused = True
                            pyautogui.click(x=x, y=y)
                            self.mainClickingPaused = False
            # Wait x seconds in-between golden cookie searches.
            time.sleep(self.GOLD_COOKIE_SEARCH_TIMER)

    def clickMainCookie(self):
        print("Clicking main cookie.")
        while self.running:
            try:
                while not self.mainClickingPaused:
                    pyautogui.click(self.cookieCoords)
                    time.sleep(0.02)
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

    def runTasks(self):
        if self.running:
            if self.gardenEnabled:
                self.tendGarden()

    def tendGarden(self):
        farmLevel = 5  # TODO: Grab from save file.
        farm = Garden(_GARDEN_SAVE_TEST, farmLevel)

    def _closeGarden(self):
        with self._lock:
            for i in range(20):
                if self.running:
                    coords = pyautogui.locateOnScreen("img/closeGarden.png", grayscale=True, confidence=0.8)
                    if coords:
                        self.mainClickingPaused = True
                        pyautogui.click(coords)
                        self.mainClickingPaused = False
                        return True
        self.mainClickingPaused = False
        return False

    def _openGarden(self):
        with self._lock:
            for i in range(20):
                if self.running:
                    coords = pyautogui.locateOnScreen("img/viewGarden.png", grayscale=True, confidence=0.8)
                    if coords:
                        self.mainClickingPaused = True
                        pyautogui.click(coords)
                        self.mainClickingPaused = False
                        return True

        self.mainClickingPaused = False
        return False
