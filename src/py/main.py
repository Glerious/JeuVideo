from modules.window import *
from modules.background import BackGround
# from modules.level_design import Block, LevelBlocks
from modules.entity import Player
from modules.configurable import global_config
from modules.frame_clock import frame_clock
from modules.constant import key_pressed

from pygame import event, display, sprite

import pygame
import sys

 
class GameSession:
    def __init__(self) -> None:
        self.window: Window = Window()
        self.background: BackGround = BackGround()
        self.player: Player = Player()
        # self.level_blocks: LevelBlocks = LevelBlocks(global_config.config, self.window.screen)

    def running(self):
        # EventHandlder
        for events in event.get():
            match events.type:
                case pygame.QUIT:
                    self.window.end()
                    sys.exit()
                case pygame.KEYDOWN:
                    key_pressed.add(events.key)
                case pygame.KEYUP:
                    key_pressed.remove(events.key)

        # Display
        self.background.update(self.window)
        self.player.update(self.window)
        # self.level_blocks.printed()

        # Physics
        self.player.is_left = True if pygame.K_q in key_pressed else False if pygame.K_d in key_pressed else self.player.is_left
        self.player.move()
        print(self.player.position)

        # Colision


        # if not self.player.dash.active:
        #     if self.key_pressed.get(pygame.K_SPACE):
        #         self.player.jump.start()
        #     if self.key_pressed.get(pygame.K_LSHIFT):
        #         self.player.dash.start()

        # Contrôle des sols et des murs
        # _blocks_collided = sprite.spritecollide(self.player.sprite, self.level_blocks.all_blocks, False, sprite.collide_rect)
        # self.player.interactive = _blocks_collided
        # self.player.sprite_update()

        display.update()

        frame_clock.update()
        self.window.clock.tick(self.window.fps)

if __name__ == "__main__":
    session = GameSession()
    while session.window.is_running:
        session.running()