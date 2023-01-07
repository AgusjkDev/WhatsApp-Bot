import os
from typing import Callable

from classes.Command import Command
from enums import Roles


def sticker_executor(
    image: str | None,
    download_image: Callable[[str], str | None],
    create_sticker: Callable[[str], bool],
    send_message: Callable[[str], None],
) -> None:
    if not image:
        return send_message("*You need to provide an image!*")

    image_path = download_image(image)
    if not image_path:
        return send_message("*We couldn't download your image!*\n\n_Try again..._")

    created = create_sticker(image_path)
    if not created:
        send_message("*We couldn't create your sticker!*\n\n_Try again..._")

    os.remove(image_path)


sticker = Command(
    name="sticker",
    parameters=[],
    description="Creates a sticker with an image that you provide.",
    roles=Roles.ALL_ROLES,
    executor=sticker_executor,
    args=["image", "_download_image", "_create_sticker", "_send_message"],
)
