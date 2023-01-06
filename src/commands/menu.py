from typing import Callable, Optional

from classes.Command import Command


def menu_executor(
    commands: list[Command], send_message: Callable[[str, Optional[bool]], None]
) -> None:
    lines = ["```Available commands```:\n"]

    for command in commands:
        lines.append(f"*{command.usage}*: _{command.description}_\n")

    send_message("\n".join(lines))


menu = Command(
    "menu",
    "/menu",
    "Returns a list of all the available commands.",
    menu_executor,
    ["_commands", "_send_message"],
)
