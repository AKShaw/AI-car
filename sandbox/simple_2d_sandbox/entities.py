import math
from abc import ABC

import pygame

from sandbox.simple_2d_sandbox.textures import Texture


class Entity(ABC):
    texture: Texture
    position: pygame.Vector2

    dt: int  # Time since last tick (for frame rate independant physics)

    def __init__(self, texture: Texture, position: pygame.Vector2):
        self.texture = texture
        self.position = position

    def draw(self, screen: pygame.Surface):
        """
        Draw the texture onto the given screen.
        Args:
            screen: The screen to draw to.
        """
        screen.blit(self.texture.texture, self.position)

    def set_dt(self, dt):
        """
        Update dt (time since last tick)
        Args:
            dt: The new value for DT.

        Returns:

        """
        self.dt = dt

    def movement(self, pressed_keys: list):
        pass


class Car(Entity):
    def __init__(self, texture: Texture, position: pygame.Vector2):
        super().__init__(texture, position)

    def movement(self, pressed_keys: list):
        forward = pressed_keys[pygame.K_w]
        backwards = pressed_keys[pygame.K_s]
        left = pressed_keys[pygame.K_a]
        right = pressed_keys[pygame.K_d]

        if forward:
            self.position = self._update_pos(
                self.position, self.dt, 300, self.texture.angle
            )
        if backwards:
            self.position = self._update_pos(
                self.position, self.dt, -300, self.texture.angle
            )

        if left:
            self.texture.rotate(-5)
        if right:
            self.texture.rotate(5)

    def _update_pos(self, current_pos: pygame.Vector2, dt, speed, heading: float):
        print(f"Heading: {heading}")
        current_x = current_pos.x
        current_y = current_pos.y

        new_x = current_x + speed * dt * math.sin(heading)
        new_y = current_y - speed * dt * math.cos(heading)

        current_pos.update(new_x, new_y)

        return current_pos
