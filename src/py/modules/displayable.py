from modules.window import Window

from pygame import Vector2, Surface, Rect
from pygame.sprite import Sprite

class Displayable(Sprite):
    def __init__(self, surface_: Surface, coordinates_: Vector2):
        super().__init__()
        self.texture: Surface = surface_.convert_alpha()
        self.rect: Rect = surface_.get_rect()
        self.position = coordinates_
        self.opacity: int = 225

    @property
    def position(self) -> Vector2:
        return Vector2(self.rect.x, self.rect.y)
    @position.setter
    def position(self, vector_: Vector2):
        self.rect.update(
            self.rect.x + vector_.x, self.rect.y + vector_.y,
            self.rect.width, self.rect.height
        )

    def update(self, window_: Window):
        window_.set_image(self.texture, self.position)

    def set_visible(self, arg_: bool):
        self.opacity = 255 if arg_ else 0
        self.texture.set_alpha(self.opacity)

    def get_visibility(self) -> int:
        return False if self.opacity == 0 else True
    
class Movable(Displayable):
    def __init__(self, surface_, coordinates_):
        super().__init__(surface_, coordinates_)
        self.last_vector: Vector2 = Vector2()

    def move(self, vector_: Vector2):
        self.last_vector = vector_
        self.rect.move_ip(vector_.x, vector_.y)

    def colliding(self, blocks_colliding_: list):
    #TODO Corriger le bugs de collision
        for _block in blocks_colliding_:
            _block: Rect = _block.rect
            if self.rect.right > _block.left and self.rect.left < _block.left:
                self.rect.right = _block.left
            elif self.rect.left < _block.right and self.rect.right > _block.right:
                self.rect.left = _block.right
            elif self.rect.top < _block.bottom and self.rect.bottom > _block.bottom:
                self.rect.top = _block.bottom
            elif self.rect.bottom > _block.top and self.rect.top < _block.top:
                self.rect.bottom = _block.top