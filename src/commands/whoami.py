from typing import Callable, Optional

from classes.Command import Command


def whoami_executor(
    name: str, number: str, send_message: Callable[[str, Optional[bool]], None]
) -> None:
    send_message(f"You are *{name}* and your phone number is *{number}*.")


whoami = Command(
    name="whoami",
    parameters=[],
    description="Tells you who you are.",
    executor=whoami_executor,
    args=["name", "number", "_send_message"],
)
