from modules.displayable import Movable
from modules.action import Static, Movement, Jump, Action
from modules.configurable import global_config, Configurable

from pygame import Vector2, Surface

class Entity(Movable, Configurable):
    def __init__(self, surface_: Surface, coordinates_: Vector2, name_: str):
        super().__init__(surface_, coordinates_)
        Configurable.__init__(self, global_config.entity, name_)
        self.speed: int = self.config["speed"]
        self.is_left: bool = True

    def update(self, window_):
        super().update(window_)

class Player(Entity):
    def __init__(self):
        path_ = "../../resources/player/"
        self.static: Static = Static(path_)
        self.movement: Movement = Movement(path_)
        self.jump: Jump = Jump(path_)
        # self.dash: Dash = Dash(path_)
        # self.grab: Grab = Grab(path_)
        super().__init__(
            self.static.animation.get_sprite(),
            Vector2(500, 0),
            "player"
        )

    def update(self, window_):
        self.update_sprite()
        super().update(window_)

    def move(self):
        # if self.dash.is_enable():
        #     _vector = self.dash.do()
        #     return
        _vector: Vector2 = self.movement.do()
        # _vector += self.jump.do(self.position, _vector)
        self.position = _vector
        super().move(_vector*self.speed)

    def update_sprite(self):
        #TODO faire la gestion des .active dans les classes move, dash, jump, grab, static
        _states = [
            # self.dash, 
            self.jump, 
            self.movement, 
            self.static#, 
            # self.grab
            ]
        for i in _states:
            i: Action
            if i.is_enable():
                i.animation.next()
                i.animation.switch_side(self.is_left)
                self.texture = i.animation.get_sprite()
                break