from modules.displayable import Movable
from modules.action import Action, Static, Dynamic, Jump, Dash
from modules.configurable import global_config, Configurable
from modules.constant import key_pressed

from pygame import Vector2, Surface
import pygame

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
        self.movement: Dynamic = Dynamic(path_)
        self.jump: Jump = Jump(path_)
        self.dash: Dash = Dash(path_)
        # self.grab: Grab = Grab(path_)
        super().__init__(
            self.static.animation.get_sprite(),
            Vector2(500, 0),
            "player"
        )

    def update(self, window_):
        self.is_left = True if pygame.K_q in key_pressed else False if pygame.K_d in key_pressed else self.is_left
        self.update_sprite()
        super().update(window_)

    def move(self, blocks_colliding_: list):
        _vector: Vector2 = self.movement.do()
        _direction: Vector2 = _vector
        _vector += self.jump.do(self.position, _vector)
        _vector = self.dash.do(_direction, _vector)
        if len(blocks_colliding_) != 0:
            _vector = Vector2()
            self.colliding(blocks_colliding_)
        super().move(_vector*self.speed)

    def update_sprite(self):
        _states = [self.dash, self.jump, self.movement, self.static#, 
            # self.grab
            ]
        for i in _states:
            i: Action
            if i.is_enable():
                i.animation.next()
                i.animation.switch_side(self.is_left)
                self.texture = i.animation.get_sprite()
                break