from typing import Callable, Optional

from classes.Database import Database
from classes.Command import Command
from utils import normalize_phone_number
from enums import Roles


def unban_executor(
    command_params: list[str],
    db: Database,
    send_message: Callable[[str, Optional[bool]], None],
) -> None:
    if not command_params:
        return send_message("```You need to provide a phone number!```")

    phone_number = command_params[0]
    normalized_phone_number = normalize_phone_number(phone_number)

    if not db.unban_user(normalized_phone_number):
        return send_message(
            f"There was an error trying to ban *{phone_number}*.\n\nTry again..."
        )

    send_message(f"*{phone_number}* has been unbanned.")


unban = Command(
    name="unban",
    parameters=["phone number"],
    description="Unbans the given phone number.",
    roles=[Roles.ADMIN],
    executor=unban_executor,
    args=["command_params", "_db", "_send_message"],
)
