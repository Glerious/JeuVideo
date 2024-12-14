from modules.displayable import Displayable, Preceding
from modules.action import Static, Move, Jump, Dash, Grab, Action
from modules.configurable import global_config, Configurable

from pygame import Vector2, Surface

class Entity(Displayable, Configurable):
    def __init__(self, surface_: Surface, name_: str):
        super().__init__(surface_)
        Configurable.__init__(self, global_config.entity, name_)
        self.preceding: Preceding = Preceding(surface_)
        self.speed: int = self.config["speed"]
        self.is_left: bool = True

    def update(self, window_):
        self.position = self.preceding.position
        return super().update(window_)

class Player(Entity):
    def __init__(self):
        path_ = "../../resources/player/"
        self.static: Static = Static(path_)
        self.move: Move = Move(path_)
        self.jump: Jump = Jump(path_)
        # self.dash: Dash = Dash(path_)
        # self.grab: Grab = Grab(path_)
        super().__init__(self.static.animation.get_sprite(), 
            "player")
        self.preceding.set_position(Vector2(500, 0))

    def update(self, window_):
        self.update_sprite()
        return super().update(window_)

    def update_preceding(self):
        # if self.dash.is_enable():
        #     _vector = self.dash.do()
        _vector: Vector2 = self.move.do()
        self.jump.base_height_calibration(_vector)
        _vector += self.jump.do(self.preceding)

            
        self.preceding.move_position(_vector*self.speed)

    def update_sprite(self):
        #TODO faire la gestion des .active dans les classes move, dash, jump, grab, static
        # self.texture.fill((0, 0, 0, 0))
        # states = [self.dash, self.jump, self.move, self.static, self.grab]
        _states = [self.move, self.static]
        for i in _states:
            i: Action
            if i.is_enable():
                i.animation.next()
                i.animation.switch_side(self.is_left)
                self.texture = i.animation.get_sprite()
                break