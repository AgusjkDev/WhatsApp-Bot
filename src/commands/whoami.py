from typing import Callable

from classes.Command import Command
from enums import Roles


def whoami_executor(
    user_name: str,
    phone_number: str,
    send_message: Callable[[str], None],
) -> None:
    send_message(f"You are *{user_name}* and your phone number is *{phone_number}*.")


whoami = Command(
    name="whoami",
    parameters=[],
    description="Tells you who you are.",
    roles=Roles.ALL_ROLES,
    executor=whoami_executor,
    args=["user_name", "phone_number", "_send_message"],
)
