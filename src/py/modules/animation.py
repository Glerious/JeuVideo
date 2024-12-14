from modules.configurable import Configurable
from modules.frame_clock import frame_clock

from pygame.time import get_ticks
from pygame.image import load
from pygame import Surface, Vector2

class Animation(Configurable):
    """
    Cette classe n'est pas héritable, elle est composable.
    Pour implémenter cette classe, il est nécéssaire d'implémenter un spritesheet.

    self.sprite_sheet = split_sprite_sheet(self, sprite_number_: Vector2, path_: str) -> list[list[Surface]]
    """
    def __init__(self, config_: dict) -> None:
        super().__init__(config_, "animation")
        self.sprite_sheet: list = []
        self.active_sprite: Vector2 = Vector2()
        self.cooldown: Cooldown = Cooldown(self.config["delay"])
    
    def split_sprite_sheet(self, path_: str) -> list[list[Surface]]:
        _sprite_sheet = load(path_)
        _width, _height = _sprite_sheet.get_size()
        _sprite_width, _sprite_height = _width//2, _height//self.config["sprite"]
        self.sprite_sheet = [
            [
                _sprite_sheet.subsurface(x, y, _sprite_width, _sprite_height) for x in range(0, _width, _sprite_width)
            ] for y in range(0, _height, _sprite_height)
        ]

    def next(self):
        if self.cooldown.in_delay():
            return
        _x = 0 if self.active_sprite.x == (len(self.sprite_sheet) - 1) and self.config["roll"] else self.active_sprite.x + 1
        self.active_sprite = Vector2(_x, self.active_sprite.y)
        self.cooldown.start()

    def switch_side(self, is_left_: bool):
        self.active_sprite = Vector2(self.active_sprite.x, 0 if is_left_ else 1)

    def get_sprite(self) -> Surface:
        return self.sprite_sheet[int(self.active_sprite.x)][int(self.active_sprite.y)]

class CooldownMS:
    def __init__(self, delay_milliseconds_: int):
        self.begin: int = 0
        self.delay: int = delay_milliseconds_

    def start(self):
        self.begin = get_ticks()

    def reset(self):
        self.begin = 0

    def in_delay(self) -> bool:
        return self.time_elapsed() < self.delay

    def time_elapsed(self) -> int:
        return get_ticks() - self.begin
    
class Cooldown:
    def __init__(self, delay_frame_: int):
        self.begin: int = 0
        self.delay: int = delay_frame_

    def start(self):
        self.begin = frame_clock.get()

    def reset(self):
        self.begin = 0

    def in_delay(self) -> bool:
        return self.time_elapsed() < self.delay
    
    def time_elapsed(self) -> int:
        return frame_clock.get() - self.begin