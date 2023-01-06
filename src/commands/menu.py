from typing import Callable, Optional

from classes.Command import Command
from enums import Roles
from constants import COMMAND_SYMBOL


def menu_executor(
    user_role: str,
    commands: dict[str, list[Command]],
    send_message: Callable[[str, Optional[bool]], None],
) -> None:
    def format_command(command: Command) -> str:
        parameters = (
            "*;*".join([f"_<{parameter}>_" for parameter in command.parameters])
            if command.parameters
            else None
        )

        return f"*{COMMAND_SYMBOL}{command.name}*{f' {parameters}' if parameters else ''}: _{command.description}_"

    lines = ["```Global commands```:\n"] + [
        format_command(command) for command in commands["global"]
    ]

    if user_role in Roles.STAFF:
        lines.extend(
            ["\n```Staff commands```:\n"]
            + [format_command(command) for command in commands["staff"]]
        )

    send_message("\n".join(lines))


menu = Command(
    name="menu",
    parameters=[],
    description="Returns a list of all the available commands.",
    roles=Roles.ALL_ROLES,
    executor=menu_executor,
    args=["user_role", "_commands", "_send_message"],
)
