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
        self.__active: bool = False
        self.duration: Cooldown = Cooldown(self.config["duration"])
        self.cooldown: Cooldown = Cooldown(self.config["cooldown"])

    def enable(self):
        if self.cooldown.in_delay() or self.is_enable():
            return
        self.__active = True
        self.animation.cooldown.start()
        self.duration.start()

    def disable(self):
        self.__active = False
        self.duration.reset()
        self.animation.cooldown.reset()
        self.cooldown.start()

    def is_enable(self):
        return self.__active
    
    def do(self) -> Vector2:
        return Vector2()

class Static(Action):
    def __init__(self, path_: str) -> None:
        super().__init__(path_ + "static.png", "static")
        self.enable()

class Dynamic(Action):
    def __init__(self, path_: str) -> None:
        super().__init__(path_ + "move.png", "move")

    def do(self) -> Vector2:
        _vector = Vector2()
        if pygame.K_d in key_pressed:
            _vector += Vector2(1, 0)
        if pygame.K_q in key_pressed:
            _vector -= Vector2(1, 0)
        if pygame.K_z in key_pressed:
            _vector -= Vector2(0, 1)
        if pygame.K_s in key_pressed:
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

    def enable(self, position_: Vector2):
        super().enable()
        self.base_height = position_.y
        self.last_height = 0

    def do(self, position_: Vector2, calibration_: Vector2) -> Vector2:
        _vector = Vector2()
        if not self.is_enable():
            if pygame.K_SPACE in key_pressed:
                self.enable(position_)
            return _vector
        self.base_height += calibration_.y
        _vector = self.__increase_vector(position_)
        return _vector

    def __increase_vector(self, position_: Vector2):
        if not self.duration.in_delay():
            self.disable()
            _correction = self.base_height - position_.y
            return Vector2(0, _correction/global_config.entity["player"]["speed"])
        _height: float = self.func(self.animation.cooldown.time_elapsed())
        _vector: int = round(_height - self.last_height)
        self.last_height = _height
        return Vector2(0, _vector)
    
    def func(self, frame_: int) -> float:
        _b = self.maximum_height
        _a = _b/(0.5*self.duration.delay)**2
        _calibred_frame: int = frame_ - 0.5*self.duration.delay
        return _a*(_calibred_frame)**2 - _b

class Dash(Action):
    def __init__(self, path_: str):
        super().__init__(path_ + "dash.png", "dash")
        self.maximum_length: float = self.config["length"]
        self.step_vector: Vector2 = Vector2()

    def enable(self, direction_: Vector2):
        super().enable()
        _step_length: int = self.maximum_length/self.duration.delay
        self.step_vector = direction_*_step_length
    
    def do(self, direction_: Vector2, vector_: Vector2) -> Vector2:
        if pygame.K_LSHIFT in key_pressed:
            self.enable(direction_)
        if self.is_enable():
            if self.duration.in_delay():
                vector_ = self.step_vector
            else:
                self.disable()
        return vector_

class Grab(Action):
    def __init__(self, path_):
        super().__init__(path_ + "grab.png", "grab")