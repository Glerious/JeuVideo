from modules.window import *
from modules.background import BackGround
from modules.player import Player
from modules.level_design import Block, LevelBlocks

import sys
from json import loads
    
class GameSession:
    def __init__(self) -> None:
        self.config: dict = self.save_default_config()
        self.window: Window = Window(self.config)
        self.background: BackGround = BackGround(self.config)
        self.player: Player = Player(self.config)
        # self.level_blocks: LevelBlocks = LevelBlocks()
        self.key_pressed: dict = {}
        self.key_values = {
                pygame.K_d : "right",
                pygame.K_q : "left",
                pygame.K_z : "above",
                pygame.K_s : "under"
            }
        self.gravity_value: float = 9.81

    def save_default_config(self):
        json_file = open("../../ressources/config.json", 'r')
        data = json_file.read()
        return loads(data)

    def running(self):
        while self.window.is_running:
            # EventHandler
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        self.window.end()
                        sys.exit()
                    case pygame.KEYDOWN:
                        self.key_pressed[event.key] = True
                    case pygame.KEYUP:
                        self.key_pressed.pop(event.key)

            #KeyPress
            for i, j in self.key_values.items():
                if self.key_pressed.get(i):
                    self.player.move.incr_vector(self.config, j)

            # if self.key_pressed.get(pygame.K_SPACE):
            #     self.player.jump.start(pygame.time.get_ticks())
            # if self.key_pressed.get(pygame.K_LSHIFT):
            #     self.player.dash()

            # Contrôle des sols et des murs

            # blocks_collided = pygame.sprite.spritecollide(self.player, self.level_blocks.all_blocks, False)

            # if len(blocks_collided) > 0:
            #     if self.key_pressed.get(pygame.K_z):
            #         self.player.rect.top = blocks_collided[0].rect.bottom + 10
            #     elif self.key_pressed.get(pygame.K_s):
            #         self.player.rect.bottom = blocks_collided[0].rect.top - 10
            #     if self.key_pressed.get(pygame.K_q):
            #         self.player.rect.left = self.player.rect.right - 1
            #     elif self.key_pressed.get(pygame.K_d):
            #         self.player.rect.right = self.player.rect.left + 1

            self.player.sprite_update()

            #ScreenUpdater
            self.window.set_image(self.background.image, (0, 0))
            self.window.set_image(self.player.sprite, self.player.rect)
            # self.level_blocks.printed(self.window.screen)
            pygame.display.update()

            self.window.clock.tick(self.window.fps)

    # def gravity_effect(self, resitance = 0):
    #     print(self.gravity_value - resitance - self.player.resistance)
    #     self.player.rect.y += self.gravity_value - resitance - self.player.resistance

session = GameSession()
session.running()