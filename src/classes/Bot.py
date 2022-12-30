import time
import os
import psutil
import subprocess
from urllib import request
from zipfile import ZipFile
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import (
    SessionNotCreatedException,
    TimeoutException,
    NoSuchElementException,
)
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .Logger import Logger
from utils import get_driver_versions, get_brave_version, show_qr, close_qr
from enums import Locators, Timeouts, Attempts, Cooldowns
from exceptions import AlreadyLoggedInException, CouldntLogInException
from constants import VERSION, BRAVE_PATH, DRIVER_ARGUMENTS


class Bot:
    # Private values
    __logger: Logger
    __driver: Chrome

    # Public values
    error: bool
    logged: bool

    def __init__(self) -> None:
        self.__logger = Logger()
        self.error = False
        self.logged = False

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

        self.__driver = self.__initialize_driver()
        if self.__driver:
            self.__logger.log("Driver initialized.", "EVENT")

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

    def __initialize_driver(self) -> Chrome | None:
        self.__logger.log("Initializing driver...", "DEBUG")

        options = ChromeOptions()
        options.binary_location = BRAVE_PATH + "\\brave.exe"
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        for argument in DRIVER_ARGUMENTS:
            options.add_argument(argument)

        try:
            return Chrome(
                service=Service(executable_path="./chromedriver.exe"), options=options
            )
        except SessionNotCreatedException:
            os.remove("chromedriver.exe")

            self.__logger.log(
                "Invalid driver version! Downloading the correct one..", "DEBUG"
            )

            if not self.__download_driver():
                self.__logger.log("Couldn't download the driver!", "ERROR")
                self.error = True

                return

            return self.__initialize_driver()

    def __await_element_load(
        self, locator: tuple, timeout: int | None = None
    ) -> WebElement | None:
        while True:
            try:
                return WebDriverWait(self.__driver, timeout if timeout else 5).until(
                    EC.presence_of_element_located(locator)
                )
            except TimeoutException:
                if not timeout:
                    continue

                return

    def login(self) -> None:
        self.__logger.log("Trying to log in...", "DEBUG")

        attempt = 1
        while True:
            try:
                self.__driver.get("https://web.whatsapp.com")

                qr = self.__await_element_load(Locators.QR, Timeouts.QR)
                if not qr:
                    try:
                        if self.__driver.find_element(*Locators.HEADER):
                            raise AlreadyLoggedInException
                    except NoSuchElementException:
                        raise CouldntLogInException

                self.__logger.log("Awaiting QR code scan...", "DEBUG")

                show_qr(qr.get_attribute("data-ref"))

                if not self.__await_element_load(Locators.HEADER, Timeouts.HEADER):
                    close_qr()

                    raise CouldntLogInException

                close_qr()

                raise AlreadyLoggedInException
            except AlreadyLoggedInException:
                self.__logger.log("Logged in.", "EVENT")
                self.logged = True

                return
            except CouldntLogInException:
                if attempt < Attempts.LOGIN:
                    self.__logger.log(
                        f"Couldn't log in! Trying again in {Cooldowns.LOGIN} seconds... ({attempt}/{Attempts.LOGIN})",
                        "ERROR",
                    )
                    time.sleep(Cooldowns.LOGIN)
                    attempt += 1

                    continue

                self.__logger.log(
                    f"Couldn't log in. ({attempt}/{Attempts.LOGIN})", "ERROR"
                )
                self.error = True

                return

    def close(self) -> None:
        try:
            self.__logger.log("Closing... Please wait!", "CLOSE")

            # As the driver.quit() method doesn't end brave browser processes,
            # the only way I found to do it was killing them manually.
            for process in psutil.process_iter():
                if (
                    process.name() == "brave.exe"
                    and "--test-type=webdriver" in process.cmdline()
                ):
                    subprocess.call(
                        f"taskkill /pid {process.pid} /f /t",
                        stderr=subprocess.DEVNULL,
                        stdout=subprocess.DEVNULL,
                    )

                    break

            os.system("pause")
        except:
            pass
