from typing import Callable


class Command:
    # Public values
    name: str
    description: str
    executor: Callable[..., None]
    args: list[str] | None

    def __init__(
        self,
        name: str,
        description: str,
        executor: Callable[..., None],
        args: list[str] | None = None,
    ) -> None:
        self.name = name
        self.description = description
        self.executor = executor
        self.args = args
