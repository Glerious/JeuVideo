import pygame
# TODO Why not working
# import initializer 

class BackGround:
    def __init__(self, path : str) -> None:
        self.image : pygame.Surface = pygame.image.load(path).convert_alpha()

    def setPath(self, path : str):
        self.image = pygame.image.load(path).convert_alpha()
