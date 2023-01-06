from typing import Callable, Optional

from classes.Command import Command


def whoami_executor(
    user_name: str,
    phone_number: str,
    send_message: Callable[[str, Optional[bool]], None],
) -> None:
    send_message(f"You are *{user_name}* and your phone number is *{phone_number}*.")


whoami = Command(
    name="whoami",
    parameters=[],
    description="Tells you who you are.",
    executor=whoami_executor,
    args=["user_name", "phone_number", "_send_message"],
)
