import psutil
from typing import Callable, Optional

from classes.Command import Command
from enums import Roles


def resources_executor(send_message: Callable[[str, Optional[bool]], None]) -> None:
    cpu_usage = f"{psutil.cpu_percent()}%"

    ram = psutil.virtual_memory()
    used_ram = f"{(ram.used / 1000000000):.2f}"
    total_ram = f"{(ram.total / 1000000000):.2f}"
    ram_usage = f"{ram.percent}%"

    lines = [
        "```Host resources usage:```\n",
        f"*CPU Usage*: {cpu_usage}",
        f"*RAM*: {used_ram}/{total_ram} GB",
        f"*RAM Usage*: {ram_usage}",
    ]

    send_message("\n".join(lines))


resources = Command(
    name="resources",
    parameters=[],
    description="Returns details about CPU and RAM usage.",
    roles=[Roles.MODERATOR, Roles.ADMIN],
    executor=resources_executor,
    args=["_send_message"],
)
