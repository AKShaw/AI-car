from enum import Enum

import pygame as pg


class DrawMode(Enum):
    """
    Controls how to draw a texture to the screen.
        Centered = Draw centered around a point
        Top Left = Draw from the top left.
    """

    CENTERED = 0
    TOP_LEFT = 1


class Texture:
    texture: pg.Surface
    angle: float = 0
    pivot: pg.Vector2

    def __init__(
        self,
        texture_image_path: str,
        display_angle: float = 0,
        scale: float = 1,
        pivot: pg.Vector2 = pg.Vector2(0, 0),
    ):
        self.pivot = pivot

        self._original_texture = pg.image.load(texture_image_path)
        self.texture = pg.image.load(texture_image_path)
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
        self._original_texture = pg.transform.smoothscale(
            self._original_texture, new_size
        )

    def rotate(self, to_angle: float):
        """
        Rotate the texture to the given angle.
        Args:
            to_angle: The angle to rotate the texture to.
        """
        self.texture = pg.transform.rotate(self._original_texture, -to_angle)
        self.angle = to_angle % 360

    def draw(
        self,
        surface: pg.Surface,
        position: pg.Vector2,
        draw_mode: DrawMode = DrawMode.CENTERED,
    ):
        """
        Draw the texture onto the given surface at a positon.
        Args:
            draw_mode: The draw mode enum.
            position: The position to draw to.
            surface: The surface to draw to.
        """

        if draw_mode == DrawMode.TOP_LEFT:
            surface.blit(self.texture, position)
        elif draw_mode == DrawMode.CENTERED:
            height = self.texture.get_height()
            width = self.texture.get_width()

            adjustment = pg.Vector2(width / 2, height / 2)
            position = position - adjustment
            surface.blit(self.texture, position)
            pg.draw.rect(
                surface, "blue", self.texture.get_rect(topleft=position), width=2
            )
        else:
            raise ValueError("Invalid draw_mode value.")
