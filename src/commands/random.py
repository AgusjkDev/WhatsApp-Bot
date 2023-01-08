import os
from random import randint
from typing import Callable

from classes.Command import Command
from utils import download_random_image, get_random_quote
from enums import Roles

MAX_RANDOM_NUMBER = 9999


def random_executor(
    command_params: list[str],
    send_message: Callable[[str], None],
    send_image: Callable[[str], bool],
) -> None:
    if not command_params:
        return send_message("*You need to provide an option!*")

    option = command_params[0].lower()
    if option not in ["number", "image", "quote"]:
        return send_message(
            "*You need to pick an option between a number, image or a quote!*"
        )

    match option:
        case "number":
            return send_message(
                f"Your random number is *{randint(0, MAX_RANDOM_NUMBER)}*."
            )
        case "image":
            image_path = download_random_image()
            if not image_path:
                return send_message(
                    "*We couldn't generate a random image!*\n\n_Try again..._"
                )

            image_sent = send_image(image_path)
            if not image_sent:
                send_message("*We couldn't send you a random image!*\n\n_Try again..._")

            return os.remove(image_path)
        case "quote":
            random_quote = get_random_quote()
            if not random_quote:
                return send_message(
                    "*We couldn't generate a random quote!*\n\n_Try again..._"
                )

            return send_message(
                f"_“{random_quote['content']}”_ *- {random_quote['author']}*."
            )


random = Command(
    name="random",
    parameters=["number | image | quote"],
    description="Replies with a random number/image/quote.",
    roles=Roles.ALL_ROLES,
    executor=random_executor,
    args=["command_params", "_send_message", "_send_image"],
)
