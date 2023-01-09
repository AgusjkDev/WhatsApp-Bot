import os
import time
from colorama import just_fix_windows_console

from constants import VERSION
from enums import Colors


def get_message_type_color(message_type: str) -> str:
    match message_type:
        case "DEBUG":
            return Colors.GREEN
        case "ALERT":
            return Colors.ORANGE
        case "EVENT":
            return Colors.BLUE
        case "ERROR":
            return Colors.RED
        case "CLOSE":
            return Colors.LIGHTBLUE
        case _:
            return Colors.RESET


class Logger:
    def __init__(self) -> None:
        os.makedirs("./logs", exist_ok=True)

        # For ANSI escape in older windows versions we can use
        # this function from colorama that fixes it for us.
        just_fix_windows_console()

    def log(self, message: str, message_type: str) -> None:
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime("%d-%m-%Y")

        formattedMessage = (
            f">> [v{VERSION} | {current_time}] ¦ [{message_type}] ¦ {message}"
        )

        print(get_message_type_color(message_type) + formattedMessage + Colors.RESET)

        with open(f"./logs/{current_date}.txt", "a+", encoding="utf-8") as f:
            f.write(formattedMessage + "\n")
