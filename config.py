import toml
import os
import logging
import textwrap

CONFIG_PATH = "config.toml"
ALWAYS_DELETE = False  # for debugging config gen


class Config:
    def __init__(self):
        self.logger = logging.getLogger("wafer")

        self.saveLocation = r"C:\Program Files (x86)\Steam\steamapps\common\Cookie Clicker\resources\app\save\save.cki"
        self.gardenEnabled = True
        self.mainAutoClickerEnabled = True
        self.goldenCookieClickerEnabled = True
        self.stockMarketEnabled = True

        self.buyLimit = -100.0
        self.sellLimit = 90.0

        if ALWAYS_DELETE:
            self.save()
        else:
            self.load()

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
            # Used with the stock minigame. The threshold at which the bot will buy a specific stock. Recommended to be
            # -120.0 < x < -80.0 in order to turn a tidy profit.
            """))
            data = _insert(data, "sellLimit", textwrap.dedent("""
            # Used with the stock minigame. The threshold at which the bot will sell a specific stock. Recommended to be
            # 20.0 < x < 100.0 in order to turn a tidy profit in a reasonable amount of time.
            """))
            f.write(data)


def _insert(src, strToFind, strToInsert):
    index = src.find(strToFind)
    return src[:index] + strToInsert + src[index:]
