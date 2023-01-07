from typing import Callable

from classes.Database import Database
from classes.Command import Command
from utils import is_valid_phone_number, normalize_phone_number
from enums import Roles


def unban_executor(
    command_params: list[str],
    db: Database,
    send_message: Callable[[str], None],
) -> None:
    if not command_params:
        return send_message("*You need to provide a phone number!*")

    phone_number = command_params[0]
    if not is_valid_phone_number(phone_number):
        return send_message(
            "*Invalid phone number!*\n\n_Copy the phone number from the user's WhatsApp profile._"
        )

    normalized_phone_number = normalize_phone_number(phone_number)

    is_unbanned = db.unban_user(normalized_phone_number)
    if is_unbanned == None:
        return send_message(
            f"*There was an error trying to unban {phone_number}*!\n\n_Try again..._"
        )

    if is_unbanned:
        return send_message(f"*{phone_number}* has been unbanned.")

    send_message(f"*{phone_number}* was not banned.")


unban = Command(
    name="unban",
    parameters=["phone number"],
    description="Unbans the given phone number.",
    roles=[Roles.ADMIN, Roles.OWNER],
    executor=unban_executor,
    args=["command_params", "_db", "_send_message"],
)
