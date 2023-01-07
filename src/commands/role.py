from typing import Callable

from classes.Database import Database
from classes.Command import Command
from utils import is_valid_phone_number, normalize_phone_number
from enums import Roles


def role_executor(
    command_params: list[str],
    db: Database,
    send_message: Callable[[str], None],
) -> None:
    if not command_params or len(command_params) < 2:
        return send_message("*You need to provide a phone number and a role name!*")

    phone_number = command_params[0]
    if not is_valid_phone_number(phone_number):
        return send_message(
            "*Invalid phone number!*\n\n_Copy the phone number from the user's WhatsApp profile._"
        )

    normalized_phone_number = normalize_phone_number(phone_number)
    role_name = command_params[1].upper()

    if role_name not in Roles.ALL_ROLES:
        return send_message("*Unknown role!*")

    if role_name == Roles.OWNER:
        return send_message("*You shouldn't give OWNER role to anyone besides you!*")

    role_given = db.set_user_role(normalized_phone_number, role_name)
    if role_given == None:
        return send_message(
            "*There was an error trying to give the role!*\n\n_Try again..._"
        )
    if role_given == False:
        return send_message("*Unknown user!*")

    send_message(f"Successfully gave role *{role_name}* to *{phone_number}*.")


role = Command(
    name="role",
    parameters=["phone number", "role name"],
    description="Sets a role for a given phone number.",
    roles=[Roles.OWNER],
    executor=role_executor,
    args=["command_params", "_db", "_send_message"],
)
