from typing import List

from mss import mss
from PIL import Image
import pyautogui


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


def locate(compareImage, monitor=1, grayscale=True, confidence=0.9) -> pyautogui.Point:
    """
    Helper function to locate an image on a screen.

    :param compareImage: The image you wish to find.
    :param monitor: The monitor number to screenshot.
    :param grayscale: Whether the image should be converted to grayscale or not before applying.
    :param confidence: How precise to
    :return: The point at which the image was found.
    """
    img = screenshot(monitor=monitor)
    box = pyautogui.locate(compareImage, img, grayscale=grayscale, confidence=confidence)
    return pyautogui.Point(x=box.left+(box.width/2), y=box.top+(box.height/2))


def locateAll(compareImage, monitor=1, grayscale=True, confidence=0.9) -> List[pyautogui.Point]:
    """
        Helper function to locate all instances of an image on a screen.

        :param compareImage: The image you wish to find.
        :param monitor: The monitor number to screenshot.
        :param grayscale: Whether the image should be converted to grayscale or not before applying.
        :param confidence: How precise to
        :return: The point at which the image was found.
        """
    img = screenshot(monitor=monitor)
    boxes = pyautogui.locateAll(compareImage, img, grayscale=grayscale, confidence=confidence)
    return [pyautogui.Point(x=box.left+(box.width/2), y=box.top+(box.height/2)) for box in boxes]
