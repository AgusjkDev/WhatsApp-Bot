from typing import Callable

from classes.Database import Database
from classes.Command import Command
from utils import is_valid_phone_number, normalize_phone_number
from enums import Roles


def ban_executor(
    command_params: list[str],
    number: str,
    db: Database,
    send_message: Callable[[str], None],
) -> None:
    if not command_params or len(command_params) < 2:
        return send_message("*You need to provide a phone number and a reason!*")

    phone_number = command_params[0]
    if not is_valid_phone_number(phone_number):
        return send_message(
            "*Invalid phone number!*\n\n_Copy the phone number from the user's WhatsApp profile._"
        )

    normalized_phone_number = normalize_phone_number(phone_number)
    reason = command_params[1]

    if normalized_phone_number == number:
        return send_message("*You can't ban yourself!*")

    is_already_banned = db.is_user_banned(normalized_phone_number)
    if is_already_banned:
        return send_message(f"*{phone_number}* was already banned.")

    if is_already_banned == False:
        banned = db.ban_user(normalized_phone_number, reason)
        if banned == False:
            return send_message("*Unknown user!*")

        if banned:
            return send_message(f"*{phone_number}* has been permanently banned.")

    send_message("*There was an error trying to ban that user!*\n\n_Try again..._")


ban = Command(
    name="ban",
    parameters=["phone number", "reason"],
    description="Bans the given phone number due to a reason.",
    roles=[Roles.ADMIN, Roles.OWNER],
    executor=ban_executor,
    args=["command_params", "number", "_db", "_send_message"],
)
