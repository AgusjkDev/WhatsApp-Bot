from typing import Callable

from classes.Command import Command


def menu_executor(
    command_symbol: str, commands: list[Command], send_message: Callable[[str], None]
) -> None:
    lines = ["```Available commands```:\n"]

    for command in commands:
        lines.append(f"*{command_symbol}{command.name}*: _{command.description}_\n")

    send_message("\n".join(lines))


menu = Command(
    "menu",
    "Returns a list of all the available commands.",
    menu_executor,
    ["_command_symbol", "_commands", "_send_message"],
)
