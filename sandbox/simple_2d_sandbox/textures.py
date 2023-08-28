import pygame


class Texture:
    texture: pygame.Surface
    angle: float = 0

    def __init__(
        self,
        texture_image_path: str,
        texture_angle: float = 0,
        display_angle: float = 0,
        scale: float = 1,
    ):
        self.texture = pygame.image.load(texture_image_path)
        self.scale(scale)

        # Change texture to have desired display angle
        self.angle = texture_angle
        print(self.angle)
        angle_delta = display_angle - texture_angle
        print(f"Changing angle by {angle_delta}")
        self.rotate(angle_delta)
        print(self.angle)

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
        self.texture = pygame.transform.smoothscale(self.texture, new_size)

    def rotate(self, by_angle: float):
        """
        Rotate the texture by the given angle.
        Args:
            by_angle: The angle to rotate (clockwise) the texture around.
        """
        self.texture = pygame.transform.rotate(self.texture, 360 - by_angle)
        self.angle = (self.angle - (360 - by_angle)) % 360
