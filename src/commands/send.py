import time
from typing import Callable

from classes.Command import Command
from utils import is_valid_phone_number


def send_executor(
    name: str,
    number: str,
    command_params: list[str],
    go_to_chat: Callable[[str], bool],
    send_message: Callable[[str], None],
) -> None:
    if not command_params or len(command_params) < 2:
        return send_message("```You need to provide a phone number and a message!```")

    phone_number, message = command_params[:2]

    if not is_valid_phone_number(phone_number):
        return send_message(
            "```Invalid phone number!```\n\nCopy the phone number from the contact's WhatsApp profile."
        )

    send_message("```Sending message...```")
    time.sleep(1)

    inside_chat = go_to_chat(phone_number)
    if inside_chat:
        send_message(f"{message}\n\nSent by: *{name}* ({number}).")


send = Command(
    "send",
    "/send _<phone number>_;_<message>_",
    "Sends a message to a specified phone number, clarifying that it is your message.",
    send_executor,
    ["name", "number", "command_params", "_go_to_chat", "_send_message"],
)
