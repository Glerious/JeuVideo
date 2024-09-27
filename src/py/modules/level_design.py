import pygame
from modules.window_properties import *

class Ground(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.rect = pygame.Rect(0, HEIGHT - 100, WIDTH, 100)
    
    def printed(self, screen : pygame.Surface):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height) -> None:
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (0, 255, 0)
        self.resistance = 10

    def printed(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect)


class LevelBlocks():
    def __init__(self) -> None:
        self.all_blocks = pygame.sprite.Group()
        self.all_blocks.add(Block(0, 612 - 12, 170, HEIGHT - 612 + 12))
        self.all_blocks.add(Block(170, 714 - 12, 170, HEIGHT - 714 + 12))
        self.all_blocks.add(Block(340, 544 - 12, 120, HEIGHT - 544 + 12))
        self.all_blocks.add(Block(460, 670 - 12, 220, HEIGHT - 670 + 12))

    def printed(self, screen: pygame.Surface):
        for block in self.all_blocks:
            block : Block
            block.printed(screen)