import time
from typing import Callable

from .Logger import Logger
from .Command import Command
from commands import commands
from constants import COMMAND_SYMBOL


class CommandHandler:
    # Private values
    __logger: Logger

    # Protected values
    _send_message: Callable[[str], None]
    _command_symbol: str
    _commands: list[Command]

    def __init__(self, logger: Logger, send_message: Callable[[str], None]) -> None:
        self.__logger = logger
        self._send_message = send_message
        self._command_symbol = COMMAND_SYMBOL
        self._commands = []

        for command in commands:
            self.__logger.log(
                f"Registering command: {self._command_symbol}{command.name}...", "DEBUG"
            )
            self._commands.append(command)

    def execute(self, name: str, number: str, message: str) -> None:
        if not message.startswith(self._command_symbol):
            return

        command_name = message[1:].split(" ")[0]

        matched_commands = [
            command for command in self._commands if command_name == command.name
        ]
        if not matched_commands:
            return self._send_message("```Unknown command!```\n\nTry using /menu")

        command = matched_commands[0]

        try:
            time_start = time.time()

            if command.args:
                command.executor(
                    *[
                        self.__getattribute__(arg)
                        if arg.startswith("_")
                        else (
                            name
                            if arg == "name"
                            else (number if arg == "number" else None)
                        )
                        for arg in command.args
                    ]
                )
            else:
                command.executor()

            total_time = f"{time.time() - time_start:.2f}"

            self.__logger.log(
                f"{name} ({number}) successfully executed a command in {total_time}s: {self._command_symbol}{command_name}",
                "EVENT",
            )
        except Exception as e:  # Only for development purposes
            self.__logger.log(
                f"There was an error handling a command: {self._command_symbol}{command_name}",
                "ERROR",
            )

            import traceback

            traceback.print_exception(e)
            print("\n", e.__class__, "\n")
