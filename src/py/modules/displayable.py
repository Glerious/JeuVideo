from modules.window import Window
from modules.level_design import Block

from pygame import Vector2, Surface, Rect
from pygame.sprite import Sprite

class Displayable(Sprite):
    def __init__(self, surface_: Surface):
        super().__init__()
        self.texture: Surface = surface_.convert_alpha()
        self.rect: Rect = surface_.get_rect()
        self.position: Vector2 = Vector2(self.rect.x, self.rect.y)
        self.opacity: int = 225

    def set_position(self, vector_: Vector2):
        self.position = vector_

    def update(self, window_: Window):
        window_.set_image(self.texture, self.position)

    def set_transparent(self):
        self.opacity = 0
        self.texture.set_alpha(self.opacity)

    def set_visible(self):
        self.opacity = 255
        self.texture.set_alpha(self.opacity)

    def get_visibility(self) -> int:
        return self.opacity
    
class Movable(Displayable):
    def __init__(self, surface_):
        super().__init__(surface_)

    def move_position(self, vector_: Vector2):
        self.position += vector_

class Preceding(Movable):
    def __init__(self, surface_):
        super().__init__(surface_)
        self.last_vector: Vector2 = Vector2()
        # self.set_transparent()

    def log_vector(self, vector_: Vector2):
        self.last_vector = vector_
        self.move_position(vector_)

    def colliding(self, blocks_colliding_: list) -> Vector2:
        _corrector = Vector2()
        for _block in blocks_colliding_:
            _block: Block
            if self.last_vector[0] > 0:
                _corrector[0] = _block.rect.left - self.rect.right
            elif self.last_vector[0] < 0:
                _corrector[0] = _block.rect.right - self.rect.left
            if self.last_vector[1] > 0:
                _corrector[1] = _block.rect.top - self.rect.bottom
            elif self.last_vector[1] < 0:
                _corrector[1] = _block.rect.bottom - self.rect.top
        return _corrector  