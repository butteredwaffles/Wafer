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

    def __init__(self, manageGarden: bool = True):
        self.cookieCoords = None
        self._lock = threading.Lock()
        self.running = True

        if manageGarden:
            self.tendGarden()

    def run(self):
        self.calibrate()
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(self.clickMainCookie), executor.submit(self.clickGoldenCookies)]

    def clickGoldenCookies(self):
        print("Beginning search for golden cookies.")
        while self.running:
            sc = pyautogui.screenshot()
            for x in range(300, sc.width-300, 5):
                for y in range(300, sc.height-300, 5):
                    pixel = sc.getpixel((x, y))
                    if pixel == self.GOLD_COOKIE_COLOR_1 or pixel == self.GOLD_COOKIE_COLOR_2:
                        print(f"Located golden cookie at ({x}, {y}). Clicking...")
                        with self._lock:
                            pyautogui.click(x=x, y=y)
                        break
            # Wait x seconds in-between golden cookie searches.
            time.sleep(self.GOLD_COOKIE_SEARCH_TIMER)

    def clickMainCookie(self):
        print("Clicking main cookie.")
        while self.running:
            try:
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

    def tendGarden(self):
        farm = Garden(_GARDEN_SAVE_TEST)
        from pprint import pprint
        pprint(farm.plots)