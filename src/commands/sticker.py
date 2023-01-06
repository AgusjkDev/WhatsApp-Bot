import os
from typing import Callable, Optional

from classes.Command import Command


def sticker_executor(
    image: str | None,
    download_image: Callable[[str], str | None],
    create_sticker: Callable[[str], None],
    send_message: Callable[[str, Optional[bool]], None],
) -> None:
    if not image:
        return send_message("```You need to provide an image!```")

    image_path = download_image(image)
    if not image_path:
        return send_message("```We couldn't download your image!```\n\nTry again...")

    create_sticker(image_path)
    os.remove(image_path)


sticker = Command(
    name="sticker",
    parameters=[],
    description="Creates a sticker with an image that you provide.",
    executor=sticker_executor,
    args=["image", "_download_image", "_create_sticker", "_send_message"],
)
