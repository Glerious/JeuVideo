from pygame import Surface, Vector2, init, quit
from pygame.display import set_caption, set_mode
from pygame.time import Clock
from modules.configurable import global_config

class Window():
    def __init__(self) -> None:
        self.is_running : bool = True
        self.screen : Surface = self.window_generator()
        self.clock = Clock()
        self.fps = global_config.window["fps"]

    def start(self):
        self.is_running = True
        return init()

    def end(self):
        self.is_running = False
        return quit()

    def window_generator(self) -> Surface:
        set_caption(global_config.window["name"])
        return set_mode((global_config.window["width"], 
                         global_config.window["height"]))
    
    def set_image(self, image_: Surface, destination_: Vector2):
        self.screen.blit(image_, destination_)