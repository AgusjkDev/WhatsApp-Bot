from typing import Callable, Optional

from classes.Database import Database
from classes.Command import Command
from utils import is_valid_phone_number, normalize_phone_number
from enums import Roles


def user_executor(
    command_params: list[str],
    db: Database,
    send_message: Callable[[str, Optional[bool]], None],
) -> None:
    if not command_params:
        return send_message("*You need to provide a phone number!*")

    phone_number = command_params[0]
    if not is_valid_phone_number(phone_number):
        return send_message(
            "*Invalid phone number!*\n\n_Copy the phone number from the user's WhatsApp profile._"
        )

    normalized_phone_number = normalize_phone_number(phone_number)
    user_information = db.get_user_information(normalized_phone_number)
    if user_information == None:
        return send_message(
            f"*There was an error trying get {phone_number} information*!\n\n_Try again..._"
        )

    if not user_information:
        return send_message("*Unknown user!*")

    lines = [f"Information about *{phone_number}*:\n"] + [
        f"*{col}*: {value}"
        for col, value in zip(
            [
                "Name",
                "Created at",
                "Role",
                "Role granted at",
                "Executed commands",
                "Is banned",
            ],
            user_information,
        )
    ]

    send_message("\n".join(lines))


user = Command(
    name="user",
    parameters=["phone number"],
    description="Returns information about an user.",
    roles=Roles.STAFF,
    executor=user_executor,
    args=["command_params", "_db", "_send_message"],
)
