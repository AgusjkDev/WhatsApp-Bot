import os
import time
from colorama import just_fix_windows_console

from constants import VERSION


COLORS = {
    "DEBUG": "\033[92m",
    "EVENT": "\033[94m",
    "ERROR": "\033[31m",
    "CLOSE": "\33[33m",
    "RESET": "\033[0m",
}


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

        print(COLORS[message_type] + formattedMessage + COLORS["RESET"])

        with open(f"./logs/{current_date}.txt", "a+", encoding="utf-8") as f:
            f.write(formattedMessage + "\n")
