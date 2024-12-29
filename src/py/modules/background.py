from modules.configurable import global_config
from modules.displayable import Displayable

from pygame import Surface, Vector2
from pygame.image import load

class BackGround(Displayable):
    def __init__(self):
        super().__init__(
            load(global_config.background["path"] + global_config.background["init"]),
            Vector2(0, 0)
            )