import pygame
from modules.gameclass import GameClass

class Window(GameClass):
    def __init__(self, config: dict) -> None:
        super().__init__(config, "window")
        self.is_running : bool = True
        self.screen : pygame.Surface = self.window_generator()
        self.clock = pygame.time.Clock()
        self.fps = self.config["fps"]

    def start(self):
        self.is_running = True
        return pygame.init()

    def end(self):
        self.is_running = False
        return pygame.quit()

    def window_generator(self) -> pygame.Surface:
        pygame.display.set_caption(self.config["name"])
        return pygame.display.set_mode((self.config["name"], self.config["height"]))
    
    def set_image(self, image : pygame.Surface, destination):
        self.screen.blit(image, destination)