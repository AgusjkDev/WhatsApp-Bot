import time
import os
import psutil
import shutil
from urllib import request
from zipfile import ZipFile
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import (
    SessionNotCreatedException,
    NoSuchElementException,
    StaleElementReferenceException,
)

from .Language import Language
from .Logger import Logger
from .Database import Database
from .CommandHandler import CommandHandler
from utils import (
    get_driver_versions,
    get_brave_version,
    await_element_load,
    open_qr,
    kill_process,
    normalize_phone_number,
)
from enums import Locators, Timeouts, Attempts, Cooldowns
from exceptions import (
    QrCodeException,
    CouldntLogInException,
    CouldntHandleMessageException,
)
from constants import BRAVE_PATH, DRIVER_ARGUMENTS, TEMP_FOLDER


class Bot:
    # Private values
    __language: Language
    __logger: Logger
    __command_handler: CommandHandler
    __driver: Chrome

    # Public values
    error: bool
    logged: bool

    def __init__(self, language: Language, logger: Logger, db: Database) -> None:
        self.__language = language
        self.__logger = logger
        self.__db = db
        self.error = False
        self.logged = False

        if "chromedriver.exe" not in os.listdir("."):
            self.__logger.log(self.__language.BOT_DRIVER_NOT_FOUND_DOWNLOADING, "DEBUG")

            downloaded = self.__download_driver()

            if not downloaded:
                self.__logger.log(self.__language.BOT_DRIVER_COULDNT_DOWNLOAD, "ERROR")
                self.error = True

                return

            self.__logger.log(self.__language.BOT_DRIVER_DOWNLOADED, "EVENT")

        self.__driver = self.__initialize_driver()
        if self.__driver:
            self.__driver.maximize_window()
            self.__logger.log(self.__language.BOT_DRIVER_INITIALIZED, "EVENT")
            self.__command_handler = CommandHandler(
                self.__driver, self.__logger, self.__language, self.__db
            )

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
        ZipFile(temp_file, "r").extract("chromedriver.exe")
        os.remove(temp_file)

        return True

    def __initialize_driver(self) -> Chrome | None:
        self.__logger.log(self.__language.BOT_DRIVER_INITIALIZING, "DEBUG")

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
                self.__language.BOT_DRIVER_INVALID_VERSION_DOWNLOADING, "DEBUG"
            )

            if not self.__download_driver():
                self.__logger.log(self.__language.BOT_DRIVER_COULDNT_DOWNLOAD, "ERROR")
                self.error = True

                return

            return self.__initialize_driver()

    def __find_pinned_chat(self) -> WebElement | None:
        attempt = 1
        while True:
            pinned_chat = await_element_load(
                Locators.PINNED_CHAT, self.__driver, timeout=Timeouts.PINNED_CHAT
            )
            if pinned_chat:
                return pinned_chat

            if attempt < Attempts.PINNED_CHAT:
                self.__driver.get("https://web.whatsapp.com")
                self.__logger.log(
                    self.__language.BOT_PINNED_CHAT_COULDNT_FIND_RETRYING.format(
                        Cooldowns.PINNED_CHAT, attempt, Attempts.PINNED_CHAT
                    ),
                    "ERROR",
                )
                time.sleep(Cooldowns.PINNED_CHAT)
                attempt += 1

                continue

            self.__logger.log(
                self.__language.BOT_PINNED_CHAT_COULDNT_FIND.format(
                    attempt, Attempts.PINNED_CHAT
                ),
                "ERROR",
            )
            self.error = True

            return

    def __get_chat_data(self) -> list[str] | None:
        try:
            self.__driver.find_element(*Locators.CHAT_HEADER).click()
            chat_info = self.__driver.find_element(*Locators.CHAT_INFO)

            try:
                return [
                    element.get_attribute("innerText")
                    for element in [
                        chat_info.find_element(*Locators.BUSINESS_NAME),
                        chat_info.find_element(*Locators.BUSINESS_NUMBER),
                    ]
                ]
            except NoSuchElementException:
                pass

            return [
                element.get_attribute("innerText").replace("~", "")
                for element in [
                    chat_info.find_element(*Locators.PERSON_NAME),
                    chat_info.find_element(*Locators.PERSON_NUMBER),
                ]
            ]
        except NoSuchElementException:
            return

    def __get_message_data(self) -> dict[str, str] | None:
        message_containers = self.__driver.find_elements(*Locators.MESSAGE_CONTAINER)
        if not message_containers:
            raise CouldntHandleMessageException

        message_container = message_containers[-1]

        try:
            message_with_text = message_container.find_element(
                *Locators.MESSAGE_WITH_TEXT
            )
            emojis = message_with_text.find_elements(*Locators.EMOJIS)
            if not emojis:
                return {"message": message_with_text.text}

            for emoji in emojis:
                emoji_char = emoji.get_attribute("data-plain-text")
                self.__driver.execute_script(
                    f"arguments[0].innerHTML='{emoji_char}'", emoji
                )

            message_with_text = message_container.find_element(
                *Locators.MESSAGE_WITH_TEXT
            )

            return {"message": message_with_text.text}
        except NoSuchElementException:
            try:
                image_with_text_container = message_container.find_element(
                    *Locators.IMAGE_WITH_TEXT_CONTAINER
                )

                try:
                    image_with_text_container.find_element(
                        *Locators.DOWNLOAD_IMAGE_CONTAINER
                    ).click()
                except NoSuchElementException:
                    pass

                if not await_element_load(
                    Locators.IMAGE_WITH_TEXT,
                    image_with_text_container,
                    timeout=Timeouts.IMAGE_WITH_TEXT,
                ):
                    raise CouldntHandleMessageException

                images_with_text = image_with_text_container.find_elements(
                    *Locators.IMAGE_WITH_TEXT
                )
                if not images_with_text:
                    raise CouldntHandleMessageException

                image_with_text = images_with_text[-1]
                image_text = image_with_text.get_attribute("alt")
                image_url = image_with_text.get_attribute("src")

                return {"message": image_text, "image": image_url}
            except NoSuchElementException:
                return

    def login(self) -> None:
        self.__logger.log(self.__language.BOT_LOGIN_TRYING, "DEBUG")

        attempt = 1
        while True:
            try:
                self.__driver.get("https://web.whatsapp.com")

                if attempt > 1:
                    if await_element_load(
                        Locators.LOGGING_IN,
                        self.__driver,
                        timeout=Timeouts.ALREADY_LOGGED_IN,
                    ):
                        self.__logger.log(
                            self.__language.BOT_LOGIN_ALREADY_LOGGED, "EVENT"
                        )
                        self.logged = True

                        return

                qr = await_element_load(Locators.QR, self.__driver, timeout=Timeouts.QR)
                if not qr:
                    raise QrCodeException

                qr_temp_file = f"{TEMP_FOLDER}\\temp-{int(time.time())}.png"
                if not qr.screenshot(qr_temp_file):
                    raise QrCodeException

                opened_qr = open_qr(qr_temp_file)
                self.__logger.log(self.__language.BOT_LOGIN_AWAITING_QR_SCAN, "DEBUG")

                if not await_element_load(
                    Locators.LOGGING_IN, self.__driver, timeout=Timeouts.LOGGING_IN
                ):
                    kill_process(*opened_qr)

                    raise CouldntLogInException

                kill_process(*opened_qr)
                self.__logger.log(self.__language.BOT_LOGIN_QR_SCANNED, "DEBUG")

                if not await_element_load(
                    Locators.HEADER, self.__driver, timeout=Timeouts.HEADER
                ):
                    raise CouldntLogInException

                self.__logger.log(self.__language.BOT_LOGIN_LOGGED, "EVENT")
                self.logged = True

                return
            except QrCodeException:
                self.__logger.log(
                    self.__language.BOT_LOGIN_QR_ERROR,
                    "ERROR",
                )

            except CouldntLogInException:
                if attempt < Attempts.LOGIN:
                    self.__logger.log(
                        self.__language.BOT_LOGIN_COULDNT_LOGIN_RETRYING.format(
                            Cooldowns.LOGIN, attempt, Attempts.LOGIN
                        ),
                        "ERROR",
                    )
                    time.sleep(Cooldowns.LOGIN)
                    attempt += 1

                    continue

                self.__logger.log(
                    self.__language.BOT_LOGIN_COULDNT_LOGIN.format(
                        attempt, Attempts.LOGIN
                    ),
                    "ERROR",
                )
                self.error = True

                return

    def handle_messages(self) -> None:
        self.__logger.log(self.__language.BOT_MESSAGE_HANDLING, "DEBUG")

        while True:
            time.sleep(0.25)

            new_chats = self.__driver.find_elements(*Locators.NEW_CHAT)
            if not new_chats:
                continue

            try:
                chat = new_chats[-1].find_element(*Locators.NEW_CHAT_CONTAINER)
            except (NoSuchElementException, StaleElementReferenceException):
                continue

            user_name, phone_number = None, None

            try:
                chat.click()

                chat_data = self.__get_chat_data()
                if chat_data:
                    user_name, phone_number = chat_data
                    number = normalize_phone_number(phone_number)
                    if self.__db.is_user_banned(number) == False:
                        message_data = self.__get_message_data()
                        if message_data:
                            self.__command_handler.execute(
                                user_name=user_name,
                                phone_number=phone_number,
                                number=number,
                                **message_data,
                            )

            except CouldntHandleMessageException:
                self.__logger.log(self.__language.BOT_MESSAGE_HANDLING_ERROR, "ERROR")

            except StaleElementReferenceException:  # If we are here and no one has been spamming, there's something wrong.
                self.__logger.log(
                    self.__language.BOT_MESSAGE_HANDLING_SPAMMING.format(
                        user_name if user_name else "An user",
                        f" ({phone_number})" if phone_number else "",
                    ),
                    "ALERT",
                )

            finally:
                pinned_chat = self.__find_pinned_chat()
                if not pinned_chat:
                    return

                pinned_chat.click()

    def close(self) -> None:
        self.__logger.log(self.__language.BOT_CLOSE_CLOSING, "CLOSE")

        # As the driver.quit() method doesn't end brave browser processes,
        # the only way I found to do it was killing them manually.
        for process in psutil.process_iter():
            try:
                if (
                    process.name() == "brave.exe"
                    and "--test-type=webdriver" in process.cmdline()
                ):
                    kill_process(process.pid)
            except:
                continue

        # After killing the browser, we need to delete all the
        # temporal files created by its instance.
        try:
            temp_folder = os.getenv("TEMP")
            if temp_folder:
                shutil.rmtree(temp_folder, ignore_errors=True)
        except:
            return
