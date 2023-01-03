from typing import Callable

from classes.Command import Command


def whoami_executor(
    name: str, number: str, send_message: Callable[[str], None]
) -> None:
    send_message(f"You are *{name}* and your phone number is *{number}*.")


whoami = Command(
    "whoami",
    "/whoami",
    "Tells you who you are.",
    whoami_executor,
    ["name", "number", "_send_message"],
)
