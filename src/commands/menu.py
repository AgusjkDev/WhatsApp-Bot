from typing import Callable, Optional

from classes.Command import Command
from constants import COMMAND_SYMBOL


def menu_executor(
    commands: list[Command], send_message: Callable[[str, Optional[bool]], None]
) -> None:
    lines = ["```Available commands```:\n"]

    for command in commands:
        parameters = (
            "*;*".join([f"_<{parameter}>_" for parameter in command.parameters])
            if command.parameters
            else None
        )
        lines.append(
            f"*{COMMAND_SYMBOL}{command.name}*{f' {parameters}' if parameters else ''}: _{command.description}_"
        )

    send_message("\n".join(lines))


menu = Command(
    name="menu",
    parameters=[],
    description="Returns a list of all the available commands.",
    executor=menu_executor,
    args=["_commands", "_send_message"],
)
