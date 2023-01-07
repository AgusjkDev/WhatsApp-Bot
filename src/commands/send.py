import time
from typing import Callable, Optional

from classes.Database import Database
from classes.Command import Command
from utils import is_valid_phone_number, normalize_phone_number
from enums import Roles


def send_executor(
    user_name: str,
    phone_number: str,
    command_params: list[str],
    db: Database,
    go_to_chat: Callable[[str], bool],
    send_message: Callable[[str, Optional[bool]], None],
) -> None:
    if not command_params or len(command_params) < 2:
        return send_message("*You need to provide phone number and message!*")

    to_phone_number, message = command_params[:2]
    normalized_to_phone_number = normalize_phone_number(phone_number)

    if db.is_user_banned(normalized_to_phone_number):
        return send_message("*This phone number is banned.*")

    if not is_valid_phone_number(to_phone_number):
        return send_message(
            "*Invalid phone number!*\n\n_Copy the phone number from the user's WhatsApp profile._"
        )

    send_message("_Sending message..._")
    time.sleep(1)

    inside_chat = go_to_chat(normalized_to_phone_number)
    if inside_chat:
        send_message(
            f"{message}\n\n_Sent by: *{user_name}* ({phone_number})._",
            sent_by_user=True,
        )


send = Command(
    name="send",
    parameters=["phone number", "message"],
    description="Sends a message to a specified phone number, clarifying that it is your message.",
    roles=Roles.ALL_ROLES,
    executor=send_executor,
    args=[
        "user_name",
        "phone_number",
        "command_params",
        "_db",
        "_go_to_chat",
        "_send_message",
    ],
)
