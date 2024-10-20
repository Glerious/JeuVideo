import pygame
from functools import wraps
from modules.player_properties import *
from modules.gameclass import GameClass

FRAME_FOR_JUMP = 500
STATIC_SPRITE_TIME = 200

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
    
    def set_position(self, x : int, y : int) -> None:
        self.rect.x = x
        self.rect.y = y

    def sprite_update(self):
        self.sprite.fill((0, 0, 0, 0))
        states = [self.dash, self.jump, self.move, self.static]
        for i in states:
            i: PlayerAnimation
            if i.isactive:
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

    @property
    def player(self):
        return self._player

    @property
    def isactive(self):
        return self._active
    
    @isactive.setter
    def switchactive(self):
        self._active = False if self._active else False

    @property
    def sprite_number(self):
        return self._sprite_number
    
    @property
    def digit(self):
        return self._digit
    
    @digit.setter
    def incr_digit(self):
        return self._digit + 1

    def next(self) -> int:
        return 0 if self.digit == (self.sprite_number - 1)  else self.incr_digit()

    def getpath(self) -> str:
        pass
    
class Static(PlayerAnimation):
    def __init__(self, player: Player) -> None:
        super().__init__(player, "static", 3)
        self.switchactive()
        self.begin: int = pygame.time.get_ticks()
        self.frame: int = self.config["frame"]

    def next(self):
        if pygame.time.get_ticks() - self.begin() :
            return self.digit
        self.begin = pygame.time.get_ticks()
        return super().next()

    def getpath(self) -> str:
        path = self.player.config["path"]
        path += "left" if self.player.is_left else "right"
        path += str(self.digit)
        path += ".png"
        return path

class Move(PlayerAnimation):
    def __init__(self, player: Player):
        super().__init__(player, "move")

        #TODO coder un déplacement vectoriel ayant pour norme la vitesse et sa direction ?
    def move_left(self):
        if self.rect.x <= 0:
            return
        self.is_left = True
        self.rect.x -= self.speed

    def move_right(self):
        if self.rect.x >= WIDTH:
            return
        self.is_left = False
        self.rect.x += self.speed

    def move_above(self):
        if self.rect.y <= 0:
            return
        self.rect.y -= self.speed
    
    def move_below(self):
        if self.rect.y >= HEIGHT:
            return
        self.rect.y += self.speed

class Jump(PlayerAnimation):
    def __init__(self, player : Player) -> None:
        super(self).__init__(player, "jump")
        self.player = player
        self.begin : int
        self.function = lambda x : (self.player.max_height / (self.frame_number / 2 ) ** 2) * x ** 2 - self.player.max_height
        self.frame_number : int = 500
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
        super().__init__(player, "dash")