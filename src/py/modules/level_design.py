from modules.configurable import global_config, Configurable
import pygame

class LevelStructures(Configurable):
    def __init__(self, config_: dict, name_: str, screen_: pygame.Surface):
        super().__init__(config_, name_)
        self.__screen: pygame.Surface = screen_
        self.__color: tuple = (0, 255, 0)
        self._rect: pygame.Rect

    @property
    def rect(self):
        return self._rect
    @rect.setter
    def rect(self, rect_: pygame.Rect):
        self._rect = rect_
        
    def set_transparent(self):
        self.__color = (0, 0, 0)

    def set_colored(self):
        self.__color = (0, 255, 0)

    def printed(self):
        pygame.draw.rect(self.__screen, self.__color, self.rect)

class Ground(LevelStructures, pygame.sprite.Sprite):
    def __init__(self, config_: dict, screen_: pygame.Surface) -> None:
        super().__init__(config_, "ground", screen_)
        pygame.sprite.Sprite.__init__(self)
        self.__size = self.config["size"]
        self.rect = pygame.Rect(0, global_config.window["height"] - self.__size, global_config.window["width"], self.__size)

    
class Block(LevelStructures, pygame.sprite.Sprite):
    def __init__(self, config_: dict, screen_: pygame.Surface, x_: int, y_: float, width_: int, height_: int) -> None:
        super().__init__(config_, "block", screen_)
        pygame.sprite.Sprite.__init__(self)
        self.resistance = 10
        self.rect = pygame.Rect(x_, y_, width_, height_)

class LevelBlocks(Configurable):
    def __init__(self, config_: dict, screen_: pygame.Surface) -> None:
        super().__init__(config_, "level_design")
        self._all_blocks: pygame.sprite.Group = pygame.sprite.Group()
        self._all_blocks.add(Block(self.config, screen_, 0, 612, 170, global_config.window["height"] - 612))
        self._all_blocks.add(Block(self.config, screen_, 170, 714, 170, global_config.window["height"] - 714))
        self._all_blocks.add(Block(self.config, screen_, 340, 544, 120, global_config.window["height"] - 544))
        self._all_blocks.add(Block(self.config, screen_, 460, 646, 152, global_config.window["height"] - 646))
        self._all_blocks.add(Block(self.config, screen_, 300, 100, 100, 100))
        # self._all_blocks.add(Block(self.config, 460, 670 - 12, 220, global_config.window["window"]["height"] - 670 + 12, screen_))
        self._ground: Ground = Ground(self.config, screen_)

    @property
    def all_blocks(self):
        return self._all_blocks
    @property
    def ground(self):
        return self._ground

    def printed(self):
        self.ground.printed()
        for _block in self.all_blocks:
            _block : Block
            _block.printed()


if __name__ == "__main__":
    pass