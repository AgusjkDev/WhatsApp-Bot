from classes.Command import Command

from .menu import menu
from .whoami import whoami
from .sticker import sticker
from .say import say
from .send import send
from .resources import resources
from .history import history

commands_dict: dict[str, list[Command]] = {
    "global": [menu, whoami, sticker, say, send],
    "staff": [resources, history],
}
