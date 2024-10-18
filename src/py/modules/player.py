import pygame
from functools import wraps
from modules.player_properties import *
from modules.gameclass import GameClass

FRAME_FOR_JUMP = 500
STATIC_SPRITE_TIME = 200

class Player(GameClass, pygame.sprite.Sprite):
    def __init__(self, config: dict) -> None:
        super(self).__init__(config, "player")
        statistics_config = self.config["statistics"]
        # Statistic
        self.max_health: int = statistics_config["health"]
        self._health: int = self.max_health
        self.max_speed: int = statistics_config["speed"]
        self._speed: int = self.max_speed
        self._mass: int = 65
        # Dynamic informations
        self._static: Static = Static(self, pygame.time.get_ticks())
        self._jump: Jump
        self._dash: Dash
        self.is_left : bool = False
        # Display
        self.sprite: pygame.Surface
        self.next_frame: pygame.Surface = pygame.image.load(self.statics.get_path()).convert_alpha()
        self.rect = self.sprite.get_rect()
        self.set_position(40, 0)
        self.sprite_update()

    @property
    def static(self):
        return self._static
    
    @static.setter
    def setstatic(self):
        self._static = Static(self, pygame.time.get_ticks())

    @static.deleter
    def delstatic(self):
        del self._static

    def set_position(self, x : int, y : int) -> None:
        self.rect.x = x
        self.rect.y = y

    def sprite_update(self):
        self.sprite.fill((0, 0, 0, 0))
        self.sprite = self.next_frame
        self.next_frame = 
        self.sprite = pygame.image.load(self.get_path()).convert_alpha()


    
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

    def dash(self):
        return
    

class PlayerAnimation(GameClass):
    def __init__(self, player: Player, name: str) -> None:
        super(self).__init__(player.config, name)
        self._player: Player = player

    @property
    def player(self):
        return self._player
    
    @player.setter
    def setplayer(self, player: Player):
        self._player = player
    
class Static(PlayerAnimation):
    def __init__(self, player: Player, time : int) -> None:
        super(self).__init__(player, "static")
        self.begin = time
        self.frame = self.player.config["frame"]

    def next(self):
        now = pygame.time.get_ticks()
        if now - self.begin >= self.cooldown:
            self.begin = now
            self.player.frame_update()


    def get_path(self) -> str:
        path = self.frame_path
        if self.is_static:
            path += "static_" + str(self.frame_number) + "_"
        path += "l" if self.is_left else "r"
        path += ".png"
        return path

    def next_frame(self) -> None:
        if self.is_static:
            self.frame_number = 0 if self.frame_number == 2 else self.frame_number + 1

class Jump():
    def __init__(self, player : Player) -> None:
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

class Dash:
    pass