import pygame
from modules.gameclass import GameClass

class BackGround(GameClass):
    def __init__(self, config : dict) -> None:
        super().__init__(config, "background")
        self._image : pygame.Surface = pygame.image.load(self.config["path"] + self.config["init"]).convert_alpha()

    @property
    def image(self):
        """Image définie pour le background."""
        return self._image

    @image.setter
    def setimage(self, name : str):
        self.image = pygame.image.load(name).convert_alpha()
