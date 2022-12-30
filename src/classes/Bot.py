import time
import os
from urllib import request
from zipfile import ZipFile

from .Logger import Logger
from utils import get_driver_versions, get_brave_version
from constants import VERSION


class Bot:
    # Private values
    __logger: Logger

    # Public values
    error: bool

    def __init__(self) -> None:
        self.__logger = Logger()
        self.error = False

        self.__logger.log(f"Starting WhatsApp Bot v{VERSION}...", "DEBUG")
        time.sleep(3)

        if "chromedriver.exe" not in os.listdir("."):
            self.__logger.log("Driver not found! Downloading it...", "DEBUG")

            downloaded = self.__download_driver()

            if not downloaded:
                self.__logger.log("Couldn't download the driver!", "ERROR")
                self.error = True

                return

            self.__logger.log("Driver downloaded successfully.", "EVENT")

    def __download_driver(self) -> bool:
        driver_versions = get_driver_versions()
        brave_version = get_brave_version()

        if not driver_versions or not brave_version:
            return False

        main_version = brave_version.split(".")[0]
        version = driver_versions[0]

        for driver_version in driver_versions:
            if driver_version.startswith(main_version):
                version = driver_version
                break

        url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_win32.zip"
        temp_file = "temp-" + str(int(time.time())) + ".zip"
        request.urlretrieve(url, temp_file)
        ZipFile(temp_file, "r").extractall()
        os.remove(temp_file)

        return True
