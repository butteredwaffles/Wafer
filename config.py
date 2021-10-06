import logging
import os
import sys
import textwrap

import toml

CONFIG_PATH = "config.toml"
ALWAYS_DELETE = False  # for debugging config gen


class Config:
    def __init__(self):
        self.logger = logging.getLogger("wafer")

        self.saveLocation = r"C:\Program Files (x86)\Steam\steamapps\common\Cookie Clicker\resources\app\save\save.cki"
        self.gardenEnabled = True
        self.mainAutoClickerEnabled = True
        self.goldenCookieClickerEnabled = True
        self.stockMarketEnabled = False

        self.buyLimit = -90.0
        self.sellLimit = 40.0

        if ALWAYS_DELETE:
            self.save()
        else:
            self.load()

        if self.stockMarketEnabled and self.gardenEnabled:
            self.logger.critical("Stock market and garden has not been configured to work at the same time! "
                                 "Toggle one or the other.")
            sys.exit(1)

    def load(self):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as f:
                try:
                    c = toml.load(f)
                    self.logger.info("Loaded config.")

                    self.saveLocation = c["saveLocation"]
                    self.mainAutoClickerEnabled = c["mainAutoClickerEnabled"]
                    self.goldenCookieClickerEnabled = c["goldenCookieClickerEnabled"]
                    self.stockMarketEnabled = c["stockMarketEnabled"]
                    self.gardenEnabled = c["gardenEnabled"]
                    self.buyLimit = c["buyLimit"]
                    self.sellLimit = c["sellLimit"]

                except (TypeError, toml.TomlDecodeError, KeyError):
                    self.logger.info("Error: Could not decode config file. Re-generating.")
                    self.save()
        else:
            self.logger.info("Generating config file.")
            self.save()

    def save(self):
        with open(CONFIG_PATH, "w") as f:
            data = toml.dumps({
                "saveLocation": self.saveLocation,
                "mainAutoClickerEnabled": self.mainAutoClickerEnabled,
                "goldenCookieClickerEnabled": self.goldenCookieClickerEnabled,
                "stockMarketEnabled": self.stockMarketEnabled,
                "gardenEnabled": self.gardenEnabled,
                "buyLimit": self.buyLimit,
                "sellLimit": self.sellLimit
            })
            data = _insert(data, "mainAutoClick", "# Toggles whether the main cookie is automatically clicked.\n")
            data = _insert(data, "goldenCookieClick", "\n# Toggles whether golden cookies are automatically clicked.\n")
            data = _insert(data, "garden", "\n# Toggles management of the garden minigame.\n")
            data = _insert(data, "stockMarket", "\n# Toggles management of the stock market minigame.\n")
            data = _insert(data, "buyLimit", textwrap.dedent("""
            # Used with the stock minigame. The threshold at which the bot will buy a specific stock, relative
            # to its resting price.
            """))
            data = _insert(data, "sellLimit", textwrap.dedent("""
            # Used with the stock minigame. The threshold at which the bot will sell a specific stock, relative
            # to its resting price.
            """))
            f.write(data)


def _insert(src, strToFind, strToInsert):
    index = src.find(strToFind)
    return src[:index] + strToInsert + src[index:]
