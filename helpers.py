import base64
import logging
from typing import List

import cv2
import numpy as np
import pyautogui
import pytesseract
from PIL import Image
from mss import mss

from config import Config

WORDS_TO_POWER = {
    "thousand": 1E3,
    "million": 1E6,
    "billion": 1E9,
    "trillion": 1E12,
    "quadrillion": 1E15,
    "quintillion": 1E18,
    "sextillion": 1E21,
    "septillion": 1E24
}


def screenshot(monitor=1) -> Image:
    """
    Helper function to screenshot a specific monitor.

    :param monitor: The number of the monitor to screenshot. Index 0 means all monitors.
    :return: A PIL Image containing the screenshot.
    :rtype: PIL.Image
    """
    with mss() as sct:
        ss = sct.grab(sct.monitors[monitor])
        img = Image.frombytes('RGB', ss.size, ss.rgb)
        return img


def locate(compareImage, monitor=1, grayscale=True, confidence=0.9, center=True) -> pyautogui.Point:
    """
    Helper function to locate an image on a screen.

    :param compareImage: The image you wish to find.
    :param monitor: The monitor number to screenshot.
    :param grayscale: Whether the image should be converted to grayscale or not before applying.
    :param confidence: How strict to be with image identification.
    :param center: Whether to return the coordinate from the center of the found image or from the top-left.
    :return: The point at which the image was found.
    """
    img = screenshot(monitor=monitor)
    box = pyautogui.locate(compareImage, img, grayscale=grayscale, confidence=confidence)
    if center:
        return pyautogui.Point(x=box.left+(box.width/2), y=box.top+(box.height/2))
    else:
        return pyautogui.Point(x=box.left, y=box.top)


def locateAll(compareImage, monitor=1, grayscale=True, confidence=0.9) -> List[pyautogui.Point]:
    """
        Helper function to locate all instances of an image on a screen.

        :param compareImage: The image you wish to find.
        :param monitor: The monitor number to screenshot.
        :param grayscale: Whether the image should be converted to grayscale or not before applying.
        :param confidence: How strict to be with image identification.
        :return: The point at which the image was found.
        """
    img = screenshot(monitor=monitor)
    boxes = pyautogui.locateAll(compareImage, img, grayscale=grayscale, confidence=confidence)
    return [pyautogui.Point(x=box.left+(box.width/2), y=box.top+(box.height/2)) for box in boxes]


def getCurrentCPS(shortNumsEnabled=True):
    coords = locate("img/cps.png", confidence=0.7, center=False)
    with mss() as sct:
        img = sct.grab(monitor={
            "top": coords.y,
            "left": coords.x,
            "width": 400,
            "height": 30,
            "mon": 1
        })

        img = Image.frombytes('RGB', img.size, img.rgb)
        # convert to grayscale
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
        # CPS text is white on black, so invert image before thresholding
        img = cv2.bitwise_not(img)
        # eliminate all non-white objects; ie everything other than the cps text
        _, img = cv2.threshold(img, 1, 255, cv2.THRESH_BINARY)

        if not shortNumsEnabled:
            cps = pytesseract.image_to_string(img, config="--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789")\
                .strip()
            return int(cps)
        else:
            strcps = pytesseract.image_to_string(img, config="--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789abcdefghilmnopqrstuvwxyz.\ ")\
                .replace("per second", "").strip()
            print(strcps)
            num, power = strcps.split(" ")[:2]
            if power in WORDS_TO_POWER:
                return int(float(num) * WORDS_TO_POWER[power])
            else:
                logging.getLogger("wafer").error("Could not locate CPS. Disable short numbers for more accuracy.")


def getCookies(config: Config):
    with open(config.saveLocation, "rb") as file:
        data = file.read().split(b"%")[0]
        missing_padding = len(data) % 4
        if missing_padding:
            data += b'=' * (4 - missing_padding)
        data = str(base64.urlsafe_b64decode(data)).split("|")[4].split(";")[0]
        return float(data)


def getHighestAscensionCPS(config: Config):
    with open(config.saveLocation, "rb") as file:
        data = file.read().split(b"%")[0]
        missing_padding = len(data) % 4
        if missing_padding:
            data += b'=' * (4 - missing_padding)
        data = str(base64.urlsafe_b64decode(data)).split("|")[4].split(";")[51]
        return float(data)
