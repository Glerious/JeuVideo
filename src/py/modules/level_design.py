from modules.configurable import global_config, Configurable
from modules.displayable import Displayable

from pygame import Surface, Rect, Vector2
from pygame.sprite import Sprite, Group
import pygame

class Block(Sprite):
    def __init__(self, 
                 screen_: Surface,
                 x_: int, y_: float,
                 width_: int, height_: int) -> None:
        Sprite.__init__(self)
        self.rect: Rect = Rect(x_, y_, width_, height_)
        self.screen: Surface = screen_
        self.color: tuple = (0, 255, 0)

    def printed(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

class Ground(Block, Configurable):
    def __init__(self, config_: dict, screen_: Surface) -> None:
        Configurable.__init__(self, config_, "ground")
        self.__size = self.config["size"]
        super().__init__(screen_,
                         0, global_config.window["height"] - self.__size, 
                         global_config.window["width"], self.__size)

class LevelBlocks():
    def __init__(self, screen_: Surface) -> None:
        self.all_blocks: Group = Group()
        # self.all_blocks.add(Block(screen_, 0, 612, 170, global_config.window["height"] - 612))
        # self.all_blocks.add(Block(screen_, 170, 714, 170, global_config.window["height"] - 714))
        # self.all_blocks.add(Block(screen_, 340, 544, 120, global_config.window["height"] - 544))
        # self.all_blocks.add(Block(screen_, 460, 646, 152, global_config.window["height"] - 646))
        self.all_blocks.add(Block(screen_, 300, 100, 100, 100))
        # self.all_blocks.add(Block(screen_, 460, 670 - 12, 220, global_config.window["height"] - 670 + 12))
        self.ground: Ground = Ground(global_config.level_design, screen_)

    def printed(self):
        for _block in self.all_blocks:
            _block : Block
            _block.printed()
        self.ground.printed()

if __name__ == "__main__":
    pass