import pyautogui
import sys
from waferData import WaferData


def calibrate():
    data = WaferData()
    print("Locating main cookie...")
    for i in range(100):
        data.cookieCoords = pyautogui.locateOnScreen("img/mainCookie.png", grayscale=True, confidence=0.5)
        if data.cookieCoords:
            print("Found main cookie.\n")
            break
    if not data.cookieCoords:
        print("Could not locate main cookie.")
    return data


if __name__ == "__main__":
    info = calibrate()
    print("Looking for golden cookies...")
    while True:
        sc = pyautogui.screenshot()
        for x in range(0, sc.width, 5):
            for y in range(0, sc.height, 5):
                pixel = sc.getpixel((x, y))
                if pixel == info.GOLD_COOKIE_COLOR or pixel == (225, 201, 111):
                    pyautogui.click(x=x, y=y)