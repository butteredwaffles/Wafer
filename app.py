import logging
from wafer import Wafer
import logging

from wafer import Wafer

if __name__ == "__main__":
    logging.basicConfig(format="[%(levelname)s][%(asctime)s][%(funcName)s] %(message)s", level=logging.INFO,
                        datefmt="%m/%d/%Y %H:%M:%S")
    app = Wafer()
    app.run()
