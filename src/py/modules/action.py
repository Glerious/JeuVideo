from modules.displayable import Movable
from modules.animation import Animation, Cooldown
from modules.configurable import global_config, Configurable
from modules.constant import key_pressed

from pygame import Vector2
import pygame

class Action(Configurable):
    def __init__(self, path_: str, name_: str) -> None:
        super().__init__(global_config.action, name_)
        self.animation: Animation = Animation(self.config)
        self.animation.split_sprite_sheet(path_)
        self.duration: int = self.config["duration"]
        self.__active: bool = False
        self.cooldown: Cooldown = Cooldown(self.config["cooldown"])

    def enable(self):
        if self.cooldown.in_delay() or self.is_enable():
            return
        self.__active = True
        self.animation.cooldown.start()

    def disable(self):
        self.__active = False
        self.cooldown.start()
        self.animation.cooldown.reset()

    def is_enable(self):
        return self.__active
    
    def do(self) -> Vector2:
        return Vector2()

class Static(Action):
    def __init__(self, path_: str) -> None:
        super().__init__(path_ + "static.png", "static")
        self.enable()

class Move(Action):
    def __init__(self, path_: str) -> None:
        super().__init__(path_ + "move.png", "move")

    def do(self) -> Vector2:
        _vector = Vector2()
        for i in key_pressed:
            match i:
                case pygame.K_d:
                    _vector += Vector2(1, 0)
                case pygame.K_q:
                    _vector -= Vector2(1, 0)
                case pygame.K_z:
                    _vector -= Vector2(0, 1)
                case pygame.K_s:
                    _vector += Vector2(0, 1)
        if _vector == Vector2():
            self.disable()
            return _vector
        else:
            self.enable()
            return _vector.normalize()

class Jump(Action):
    def __init__(self, path_: str) -> None:
        super().__init__(path_ + "jump.png", "jump")
        self.maximum_height: int = self.config["height"]
        self.base_height: int = 0
        self.last_height: int = 0

    def enable(self, movable_: Movable):
        super().enable()
        self.base_height = movable_.position.x
        self.last_height = 0

    def do(self, movable_: Movable) -> Vector2:
        _vector = Vector2()
        if self.is_enable():
            _vector += self.__increase_vector(movable_)
            # print(_vector)
        for i in key_pressed:
            if i == pygame.K_SPACE:
                self.enable(movable_)
        return _vector

    def __increase_vector(self, movable_: Movable):
        if not self.animation.cooldown.in_delay():
            self.disable()
            _correction = movable_.rect.y - self.base_height
            return Vector2(0, -_correction)
        # print(self.animation.cooldown.time_elapsed())

        _height: float = self.func(self.animation.cooldown.time_elapsed())
        # print(_height)
        _vector: int = round(_height - self.last_height)
        print(_vector)
        self.last_height = _height
        return Vector2(0, _vector)
    
    def func(self, frame_: int) -> float:
        _b = self.maximum_height
        _a = _b/(0.5*self.duration)**2
        _calibred_frame: int = frame_ - 0.5*self.duration
        return _a*(_calibred_frame)**2 - _b
        
    def base_height_calibration(self, vector_: Vector2):
        self.base_height += vector_.x

class Dash(Action):
    def __init__(self, path_: str):
        super().__init__(path_ + "dash.png", "dash")
        self._maximum_length: float = self.config["length"]

    # def norm(self) -> Vector2:
    #     if frame_clock.get() - self.begin > self.frame:
    #         self.stop()
    #         return 1
    #     return self.maximum_length/(self.frame*global_config.window["speed_frame"])

class Grab(Action):
    def __init__(self, path_):
        super().__init__(path_ + "grab.png", "grab")