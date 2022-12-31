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
    StaleElementReferenceException,
)
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .Logger import Logger
from utils import get_driver_versions, get_brave_version, show_qr, close_qr
from enums import Locators, Timeouts, Attempts, Cooldowns
from exceptions import (
    AlreadyLoggedInException,
    CouldntLogInException,
    CouldntHandleMessageException,
)
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

    def __find_pinned_chat(self) -> WebElement | None:
        attempt = 1
        while True:
            pinned_chat = self.__await_element_load(
                Locators.PINNED_CHAT, Timeouts.PINNED_CHAT
            )
            if pinned_chat:
                return pinned_chat

            if attempt < Attempts.PINNED_CHAT:
                self.__driver.get("https://web.whatsapp.com")
                self.__logger.log(
                    f"Couldn't find a pinned chat to focus on! Trying again in {Cooldowns.PINNED_CHAT} seconds... ({attempt}/{Attempts.PINNED_CHAT})",
                    "ERROR",
                )
                time.sleep(Cooldowns.PINNED_CHAT)
                attempt += 1

                continue

            self.__logger.log(
                f"Couldn't find a pinned chat to focus on. ({attempt}/{Attempts.PINNED_CHAT})",
                "ERROR",
            )
            self.error = True

            return

    def __get_contact_data(self) -> list[str] | None:
        try:
            contact_info = self.__driver.find_element(*Locators.CONTACT_INFO)

            try:
                return [
                    element.get_attribute("innerText")
                    for element in [
                        contact_info.find_element(*Locators.BUSINESS_ACCOUNT_NAME),
                        contact_info.find_element(*Locators.BUSINESS_ACCOUNT_NUMBER),
                    ]
                ]
            except NoSuchElementException:
                pass

            name_or_number, alias_or_number = [
                element.get_attribute("innerText")
                for element in [
                    contact_info.find_element(*Locators.CONTACT_NAME_OR_NUMBER),
                    contact_info.find_element(*Locators.CONTACT_ALIAS_OR_NUMBER),
                ]
            ]

            return (
                [alias_or_number[1:], name_or_number]
                if alias_or_number.startswith("~")
                else [name_or_number, alias_or_number]
            )
        except NoSuchElementException:
            return

    def __get_message_data(self, message_container: WebElement) -> object | None:
        try:
            text_container = message_container.find_element(*Locators.TEXT_CONTAINER)
            emojis = text_container.find_elements(*Locators.EMOJIS)
            if not emojis:
                return {"type": "text", "value": text_container.text}

            if not text_container.text:
                return {"type": "invalid"}

            for emoji in emojis:
                emoji_char = emoji.get_attribute("data-plain-text")
                self.__driver.execute_script(
                    f"arguments[0].innerHTML='{emoji_char}'", emoji
                )

            updated_text_container = message_container.find_element(
                *Locators.TEXT_CONTAINER
            )

            return {"type": "text", "value": updated_text_container.text}
        except NoSuchElementException:
            for locator in [
                Locators.ONLY_EMOJIS,
                Locators.AUDIO,
                Locators.STICKER,
                Locators.IMAGE_CONTAINER,
                Locators.VIDEO,
                Locators.GIF,
                Locators.VIEW_ONCE,
                Locators.DOCUMENT,
                Locators.LOCATION,
                Locators.CONTACT,
                Locators.POLL,
                Locators.DELETED,
            ]:
                try:
                    if message_container.find_element(*locator):
                        return {"type": "invalid"}
                except NoSuchElementException:
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

    def handle_messages(self) -> None:
        self.__logger.log("Handling messages...", "DEBUG")

        pinned_chat = self.__find_pinned_chat()
        if not pinned_chat:
            return

        while True:
            new_chats = self.__driver.find_elements(*Locators.NEW_CHAT)
            if not new_chats:
                time.sleep(0.5)

                continue

            for chat in new_chats:
                name, number = None, None

                time.sleep(0.5)

                try:
                    chat.click()

                    self.__driver.find_element(*Locators.CHAT_HEADER).click()

                    contact_data = self.__get_contact_data()
                    if not contact_data:
                        raise CouldntHandleMessageException

                    name, number = contact_data

                    messages_containers = self.__driver.find_elements(
                        *Locators.MESSAGE_CONTAINER
                    )
                    if not messages_containers:
                        raise CouldntHandleMessageException

                    message_data = self.__get_message_data(messages_containers[-1])
                    if not message_data:
                        raise CouldntHandleMessageException

                    if message_data["type"] == "text":
                        self.__logger.log(
                            f"{name} ({number}): {message_data['value']}", "DEBUG"
                        )

                    time.sleep(1)
                    pinned_chat.click()
                except StaleElementReferenceException:
                    self.__logger.log(
                        f"{name if name else 'An user'}{f' ({number})' if number else ''} is probably spamming messages!",
                        "ALERT",
                    )
                except CouldntHandleMessageException:
                    self.__logger.log(
                        "There was an error handling a message, proceeding.", "ERROR"
                    )

                    time.sleep(1)
                    pinned_chat.click()

    def close(self) -> None:
        self.__logger.log("Closing... Please wait!", "CLOSE")

        # As the driver.quit() method doesn't end brave browser processes,
        # the only way I found to do it was killing them manually.
        for process in psutil.process_iter():
            try:
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
            except:
                continue

        os.system("pause")
