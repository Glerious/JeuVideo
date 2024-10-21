from modules.gameclass import GameClass

from numpy import array, ndarray
from numpy.linalg import norm
from functools import wraps
import pygame


class Player(GameClass, pygame.sprite.Sprite):
    def __init__(self, config: dict) -> None:
        super().__init__(config, "player")
        statistics_config = self.config["statistics"]
        # Statistic
        self.max_health: int = statistics_config["health"]
        self._health: int = self.max_health
        self.max_speed: int = statistics_config["speed"]
        self._speed: int = self.max_speed
        self._mass: int = statistics_config["mass"]
        # Dynamic informations
        self.static: Static = Static(self)
        self.jump: Jump = Jump(self)
        self.move: Move = Move(self)
        self.dash: Dash = Dash(self)
        self.is_left : bool = False
        # Display
        self.sprite: pygame.Surface = pygame.image.load(self.static.getpath()).convert_alpha()
        self.rect = self.sprite.get_rect()
        self.set_position(40, 0)
    
    def get_position(self) -> tuple[int, int]:
        return (self.rect.x, self.rect.y)
    
    def set_position(self, x: int, y: int) -> None:
        self.rect.x = x
        self.rect.y = y

    def incr_position(self, vector: ndarray) -> None:
        self.rect.x += vector[0]
        self.rect.y += vector[1]
                
    def position_update(self):
        vector: ndarray = self.move.vector * self.max_speed
        vector = (1 / norm(self.move.vector)) * vector if norm(self.move.vector) != 0 else vector

        # self.move.active = False if vector == array([0, 0]) else True
        self.move.reset_vector()
        self.incr_position(vector)

    def sprite_update(self):
        self.sprite.fill((0, 0, 0, 0))
        self.position_update()
        states = [self.dash, self.jump, self.move, self.static]
        for i in states:
            i: PlayerAnimation
            if i.active:
                i.next()
                self.sprite = pygame.image.load(i.getpath()).convert_alpha()
                return

class PlayerAnimation(GameClass):
    def __init__(self, player: Player, name: str, sprite_number: int) -> None:
        super().__init__(player.config, name)
        self._player: Player = player
        self._active: bool = False
        self._sprite_number: int = sprite_number
        self._digit: int = 0
        self._frame: int = self.config["frame"]
        self._begin: int = 0

    @property
    def player(self):
        return self._player

    @property
    def active(self):
        return self._active
    
    @active.setter
    def active(self, value: bool):
        self._active = value
    
    def switch_active(self):
        self._active = False if self._active else True

    @property
    def sprite_number(self):
        return self._sprite_number
    
    @property
    def digit(self):
        return self._digit
    
    @digit.setter
    def digit(self, digit: int):
        self._digit = digit
    
    @property
    def frame(self):
        return self._frame
    
    @property
    def begin(self):
        return self._begin
    
    @begin.setter
    def begin(self, time: int):
        self._begin = time
    
    def begin_now(self):
        self._begin = pygame.time.get_ticks()

    def next(self) -> int:
        if pygame.time.get_ticks() - self._begin < self._frame:
            return self.digit
        self.begin_now()
        self.digit = 0 if self.digit == (self.sprite_number - 1)  else self.digit + 1

    def get_path(self) -> str:
        pass

class Static(PlayerAnimation):
    def __init__(self, player: Player) -> None:
        super().__init__(player, "static", 3)
        self.switch_active()
        self.begin_now()

    def getpath(self) -> str:
        path = self.player.config["path"] + "static/"
        path += "left" if self.player.is_left else "right"
        path += "_" + str(self.digit)
        path += ".png"
        return path

class Move(PlayerAnimation):
    def __init__(self, player: Player):
        super().__init__(player, "move", 2)
        self._vector: ndarray = array([0, 0])

    @property
    def vector(self):
        return self._vector
    
    def reset_vector(self):
        self._vector = array([0, 0])
    
    def incr_vector(self, config: dict, name: str):
        self._vector += self.get_absolute_vector(config, name)

    def get_absolute_vector(self, config: dict, name: str) -> ndarray:
        direction = config["constant"][name]
        return array([direction["x"], direction["y"]])
    
    def get_path(self) -> str:
        path = self.player.config["path"] + "move/"
        path += "left" if self.player.is_left else "right"
        path += "_" + str(self.digit)
        path += ".png"
        return path

class Jump(PlayerAnimation):
    def __init__(self, player : Player) -> None:
        super().__init__(player, "jump", 1)
        self.function = lambda x : (self.player.max_height / (self.frame_number / 2 ) ** 2) * x ** 2 - self.player.max_height
        self.last_elevation : int = 0

    def start(self, time : int):
        # Le Jump ne se réalise pas forcement
        if self.player.is_jumping:
            return
        self.begin = time
        self.player.is_jumping = True
        self.player.is_static = False
        self.player.resistance = 10
    
    def stop(self):
        self.player.is_jumping = False
        self.player.is_static = True
        self.player.resistance = 0
        return
    
    def step(self):
        current = pygame.time.get_ticks()
        x = current - self.begin - self.frame_number / 2
        if x > 250:
            x = 250
        y = round(self.function(x))
        self.player.rect.y += (y - self.last_elevation)
        self.last_elevation = y
        if y >= 0:
            self.stop()

class Dash(PlayerAnimation):
    def __init__(self, player : Player):
        super().__init__(player, "dash", 1)