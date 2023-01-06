import os
import time
import base64
from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from .Logger import Logger
from .Database import Database
from .Command import Command
from commands import commands
from utils import await_element_load
from enums import Locators, Timeouts
from exceptions import CouldntHandleCommandException
from constants import COMMAND_SYMBOL

from traceback import print_exception  # Only for development purposes


class CommandHandler:
    # Private values
    __driver: Chrome
    __logger: Logger

    # Protected values
    _db: Database
    _commands: list[Command]

    def __init__(self, driver: Chrome, logger: Logger, db: Database) -> None:
        self.__driver = driver
        self.__logger = logger
        self._db = db
        self._commands = []

        for command in commands:
            self.__logger.log(
                f"Registering command: {COMMAND_SYMBOL}{command.name}...", "DEBUG"
            )
            self._commands.append(command)

    def _send_message(self, message: str, sent_by_user: bool = False) -> None:
        input_box = self.__driver.find_element(*Locators.INPUT_BOX)

        if not sent_by_user:
            lines = message.split("\n")
            lines_length = len(lines)
            for index, line in enumerate(lines, start=1):
                input_box.send_keys(line)

                if index != lines_length:
                    ActionChains(self.__driver).key_down(Keys.SHIFT).send_keys(
                        Keys.ENTER
                    ).key_up(Keys.SHIFT).perform()
        else:
            # If we don't type anything, the input box text element won't exist.
            input_box.send_keys(" ")
            input_box_text = input_box.find_element(*Locators.INPUT_BOX_TEXT)

            self.__driver.execute_script(
                """
                    const [element, text] = arguments;
                    const dataTransfer = new DataTransfer();
                    dataTransfer.setData("text", text);
                    const event = new ClipboardEvent("paste", {
                        clipboardData: dataTransfer,
                        bubbles: true
                    });
                    element.dispatchEvent(event)
                """,
                input_box_text,
                message,
            )

        input_box.send_keys(Keys.ENTER)

    def _download_image(self, image: str) -> str | None:
        result = self.__driver.execute_async_script(
            """
            const toBase64=_=>{for(var e,n=new Uint8Array(_),o=n.length,r=new Uint8Array(4*Math.ceil(o/3)),c=new Uint8Array(64),t=0,a=0;64>a;++a)c[a]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charCodeAt(a);for(a=0;o-o%3>a;a+=3,t+=4)e=n[a]<<16|n[a+1]<<8|n[a+2],r[t]=c[e>>18],r[t+1]=c[e>>12&63],r[t+2]=c[e>>6&63],r[t+3]=c[63&e];return o%3==1?(e=n[o-1],r[t]=c[e>>2],r[t+1]=c[e<<4&63],r[t+2]=61,r[t+3]=61):o%3==2&&(e=(n[o-2]<<8)+n[o-1],r[t]=c[e>>10],r[t+1]=c[e>>4&63],r[t+2]=c[e<<2&63],r[t+3]=61),new TextDecoder("ascii").decode(r)};

            const [url, callback] = arguments;
            fetch(url)
                .then(response => response.arrayBuffer())
                .then(arrayBuffer => callback(toBase64(arrayBuffer)))
                .catch(() => callback());
            """,
            image,
        )
        if not result:
            return

        image_path = f"{os.getenv('TEMP') or os.getcwd()}\\temp-{int(time.time())}.jpg"

        with open(image_path, "wb") as f:
            f.write(base64.b64decode(result))

        return image_path

    def _create_sticker(self, image_path: str) -> None:
        self.__driver.find_element(*Locators.EMOJI_MENU).click()
        self.__driver.find_element(*Locators.FILE_INPUT).send_keys(image_path)

        send_button = await_element_load(
            Locators.SEND_BUTTON, self.__driver, timeout=Timeouts.SEND_BUTTON
        )
        if not send_button:
            raise CouldntHandleCommandException

        send_button.click()

        await_element_load(
            Locators.PENDING_MESSAGE, self.__driver, timeout=Timeouts.PENDING_MESSAGE
        )

    def _go_to_chat(self, phone_number: str) -> bool:
        self.__driver.get(f"https://web.whatsapp.com/send/?phone={phone_number}")

        if not await_element_load(
            Locators.INPUT_BOX, self.__driver, timeout=Timeouts.INPUT_BOX
        ):
            try:
                self.__driver.find_element(*Locators.POPUP_OK_BUTTON).click()

                return False
            except NoSuchElementException:
                # One last try to find the input box.
                try:
                    if self.__driver.find_element(*Locators.INPUT_BOX):
                        return True
                except NoSuchElementException:
                    return False

        return True

    def execute(self, **kwargs) -> None:
        message = kwargs.get("message")

        if not message.startswith(COMMAND_SYMBOL):
            return

        command_name = message[1:].split(" ")[0].lower()

        try:
            kwargs["command_params"] = message[message.index(" ") + 1 :].split(";")
        except ValueError:
            pass

        matched_commands = [
            command for command in self._commands if command_name == command.name
        ]
        if not matched_commands:
            return self._send_message(
                f"```Unknown command!```\n\nTry using {COMMAND_SYMBOL}menu"
            )

        command = matched_commands[0]

        try:
            time_start = time.time()

            if command.args:
                command.executor(
                    *[
                        self.__getattribute__(arg)
                        if arg.startswith("_")
                        else kwargs.get(arg)
                        for arg in command.args
                    ]
                )
            else:
                command.executor()

            total_time = f"{time.time() - time_start:.2f}"

            self.__logger.log(
                f"{kwargs.get('user_name')} ({kwargs.get('phone_number')}) successfully executed a command in {total_time}s: {COMMAND_SYMBOL}{command_name}",
                "EVENT",
            )
            self._db.executed_command(
                kwargs.get("number"), kwargs.get("user_name"), command_name
            )
        except BaseException as e:
            self.__logger.log(
                f"There was an error handling a command: {COMMAND_SYMBOL}{command_name}",
                "ERROR",
            )

            print_exception(e)
