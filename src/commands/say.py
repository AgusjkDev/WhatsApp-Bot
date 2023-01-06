from typing import Callable, Optional

from classes.Command import Command


def say_executor(
    command_params: list[str], send_message: Callable[[str, Optional[bool]], None]
) -> None:
    if not command_params:
        return send_message("```You need to provide a message!```")

    send_message(";".join(command_params), sent_by_user=True)


say = Command(
    name="say",
    parameters=["message"],
    description="Replies with the message you sent.",
    executor=say_executor,
    args=["command_params", "_send_message"],
)
