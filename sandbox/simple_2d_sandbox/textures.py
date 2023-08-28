import pygame


class Texture:
    texture: pygame.Surface
    angle: float = 0
    pivot: pygame.Vector2

    def __init__(
        self,
        texture_image_path: str,
        display_angle: float = 0,
        scale: float = 1,
        pivot: pygame.Vector2 = pygame.Vector2(0, 0),
    ):
        self.pivot = pivot

        self._original_texture = pygame.image.load(texture_image_path)
        self.texture = pygame.image.load(texture_image_path)
        self.scale(scale)

        # Change texture to have desired display angle
        self.rotate(display_angle)

    def scale(self, scale: float):
        """
        Scale the texture by some proportion.
        Args:
            texture: The texture to rescale.
            scale: The proportion to scale the texture by.
        """
        (current_height, current_width) = (
            self.texture.get_height(),
            self.texture.get_width(),
        )

        new_size = (current_width * scale, current_height * scale)
        self._original_texture = pygame.transform.smoothscale(
            self._original_texture, new_size
        )

    def rotate(self, to_angle: float):
        """
        Rotate the texture to the given angle.
        Args:
            to_angle: The angle to rotate the texture to.
        """
        # TODO: Rotate around center
        self.texture = pygame.transform.rotate(self._original_texture, -to_angle)
        self.angle = to_angle % 360
