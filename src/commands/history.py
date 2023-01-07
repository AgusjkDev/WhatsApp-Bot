from typing import Callable, Optional

from classes.Database import Database
from classes.Command import Command
from utils import normalize_phone_number
from enums import Roles
from constants import COMMAND_SYMBOL

HISTORY_LIMIT = 25


def history_executor(
    command_params: list[str],
    db: Database,
    send_message: Callable[[str, Optional[bool]], None],
) -> None:
    if not command_params:
        return send_message("*You need to provide a phone number!*")

    phone_number = command_params[0]
    normalized_phone_number = normalize_phone_number(phone_number)

    try:
        limit = int(command_params[1]) if len(command_params) > 1 else HISTORY_LIMIT
    except ValueError:
        return send_message("*The limit must be an integer number!*")

    command_history = db.get_user_command_history(normalized_phone_number, limit)
    if not command_history:
        return send_message(f"There is no commands in the history of *{phone_number}*.")

    lines = [f"History of *{phone_number}*:\n"] + [
        f"*{COMMAND_SYMBOL}{command_name}* => {date_and_time}"
        for (command_name, date_and_time) in command_history
    ]

    send_message("\n".join(lines))


history = Command(
    name="history",
    parameters=["phone number", "limit?"],
    description="Returns the command history of an user, with an optional limit.",
    roles=Roles.STAFF,
    executor=history_executor,
    args=["command_params", "_db", "_send_message"],
)
