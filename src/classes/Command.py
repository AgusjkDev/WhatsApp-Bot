from typing import Callable


class Command:
    # Public values
    name: str
    parameters: str
    description: str
    executor: Callable[..., None]
    args: list[str] | None

    def __init__(
        self,
        name: str,
        parameters: list[str],
        description: str,
        executor: Callable[..., None],
        args: list[str] | None = None,
    ) -> None:
        self.name = name
        self.parameters = parameters
        self.description = description
        self.executor = executor
        self.args = args
