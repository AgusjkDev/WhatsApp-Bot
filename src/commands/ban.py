from typing import Callable, Optional

from classes.Database import Database
from classes.Command import Command
from utils import normalize_phone_number
from enums import Roles


def ban_executor(
    command_params: list[str],
    number: str,
    db: Database,
    send_message: Callable[[str, Optional[bool]], None],
) -> None:
    if not command_params or len(command_params) < 2:
        return send_message("```You need to provide a phone number and a reason!```")

    phone_number, reason = command_params[:2]
    normalized_phone_number = normalize_phone_number(phone_number)

    if normalized_phone_number == number:
        return send_message("```You can't ban yourself!```")

    if db.is_user_banned(normalized_phone_number):
        return send_message(f"*{phone_number}* was already banned!")

    banned = db.ban_user(normalized_phone_number, reason)
    if banned is None:
        return send_message(
            "```There was an error trying to ban that user!```\n\nTry again..."
        )

    if not banned:
        return send_message("```Unknown user!```")

    send_message(f"*{phone_number}* has been permanently banned.")


ban = Command(
    name="ban",
    parameters=["phone number", "reason"],
    description="Bans the given phone number due to a reason.",
    roles=[Roles.ADMIN],
    executor=ban_executor,
    args=["command_params", "number", "_db", "_send_message"],
)
