from typing import Callable, Optional

from classes.Database import Database
from classes.Command import Command
from enums import Roles
from constants import COMMAND_SYMBOL


def executions_executor(
    command_params: list[str],
    db: Database,
    send_message: Callable[[str, Optional[bool]], None],
) -> None:
    if not command_params:
        return send_message("```You need to provide a command name!```")

    command_name = command_params[0].replace(COMMAND_SYMBOL, "")
    command_executions = db.get_command_executions(command_name)
    if command_executions is None:
        return send_message("```Unknown command!```")

    send_message(
        f"*{COMMAND_SYMBOL}{command_name}* has been executed *{command_executions} {'times' if command_executions != 1 else 'time'}*."
    )


executions = Command(
    name="executions",
    parameters=["command name"],
    description="Returns the number of times a command has been executed.",
    roles=Roles.STAFF,
    executor=executions_executor,
    args=["command_params", "_db", "_send_message"],
)
