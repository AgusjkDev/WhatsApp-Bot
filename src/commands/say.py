from typing import Callable

from classes.Command import Command


def say_executor(
    command_params: list[str], send_message: Callable[[str], None]
) -> None:
    if not command_params:
        return send_message("```You need to provide a message!```")

    send_message(";".join(command_params))


say = Command(
    "say",
    "/say _<message>_",
    "Replies with the message you sent.",
    say_executor,
    ["command_params", "_send_message"],
)
