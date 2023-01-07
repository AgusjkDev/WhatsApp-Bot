from typing import Callable

from classes.Command import Command
from enums import Roles


def say_executor(
    command_params: list[str], send_message: Callable[[str], None]
) -> None:
    if not command_params:
        return send_message("*You need to provide a message!*")

    send_message(";".join(command_params))


say = Command(
    name="say",
    parameters=["message"],
    description="Replies with the message you sent.",
    roles=Roles.ALL_ROLES,
    executor=say_executor,
    args=["command_params", "_send_message"],
)
