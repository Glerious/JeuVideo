from modules.window import *
from modules.background import BackGround
from modules.player import Player
from modules.level_design import Block, LevelBlocks

import sys
from json import loads

class Server:
    def __init__(self):
        self.config: dict = self.save_default_config()
        self.window = Window(self.config)

    def save_default_config():
        json_file = open("../../ressources/config.json", 'r')
        data = json_file.read()
        return loads(data)

class GameSession:
    def __init__(self) -> None:
        self.server = Server()
        self.background = BackGround(self.server.config)
        self.player = Player(self.server.config)
        self.level_blocks = LevelBlocks()
        self.key_pressed = {}
        self.gravity_value = 10

    def running(self):
        
        while self.window.is_running:

            #ScreenUpdater
            window.set_image(self.background.image, (0, 0))
            window.set_image(self.player.frame, self.player.rect)
            self.level_blocks.printed(window.screen)
            pygame.display.update()

            #KeyPress
            if self.key_pressed.get(pygame.K_z):
                self.player.move_above()
            elif self.key_pressed.get(pygame.K_s):
                self.player.move_below()



            if self.key_pressed.get(pygame.K_q):
                self.player.move_left()
            elif self.key_pressed.get(pygame.K_d):
                self.player.move_right()
            if self.key_pressed.get(pygame.K_SPACE):
                self.player.jump.start(pygame.time.get_ticks())
            if self.key_pressed.get(pygame.K_LSHIFT):
                self.player.dash()

            # EventHandler
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        window.end()
                        sys.exit()
                    case pygame.KEYDOWN:
                        self.key_pressed[event.key] = True
                    case pygame.KEYUP:
                        self.key_pressed.pop(event.key)

            if self.player.is_static:
                self.player.static_animation.next()
            
            if self.player.is_jumping:
                self.player.jump.step()

            # Contrôle des sols et des murs

            blocks_collided = pygame.sprite.spritecollide(self.player, self.level_blocks.all_blocks, False)

            if len(blocks_collided) > 0:
                print("yes")
                if self.key_pressed.get(pygame.K_z):
                    self.player.rect.top = blocks_collided[0].rect.bottom + 10
                elif self.key_pressed.get(pygame.K_s):
                    self.player.rect.bottom = blocks_collided[0].rect.top - 10
                if self.key_pressed.get(pygame.K_q):
                    self.player.rect.left = self.player.rect.right - 1
                elif self.key_pressed.get(pygame.K_d):
                    self.player.rect.right = self.player.rect.left + 1

            # Contrôle de la Gravité

            window.clock.tick(window.fps)

    def gravity_effect(self, resitance = 0):
        print(self.gravity_value - resitance - self.player.resistance)
        self.player.rect.y += self.gravity_value - resitance - self.player.resistance

session = GameSession()
session.running()

