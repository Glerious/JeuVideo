import pygame

class Window:
    def __init__(self, name : str, width : float, height : float, fps : float = 60) -> None:
        self.is_running : bool = True
        self.screen : pygame.Surface = self.window_generator(name, width, height)
        self.clock = pygame.time.Clock()
        self.fps = 60


    def start(self):
        self.is_running = True
        return pygame.init()

    def end(self):
        self.is_running = False
        return pygame.quit()
    

    def window_generator(self, name : str, width : float, height : float) -> pygame.Surface:
        pygame.display.set_caption(name)
        return pygame.display.set_mode((width, height))
    
    def set_image(self, image : pygame.Surface, destination):
        self.screen.blit(image, destination)