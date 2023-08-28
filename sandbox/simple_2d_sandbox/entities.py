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
    ACCELERATION_CONST = 2
    REVERSE_CONST = 1
    COASTING_CONST = 0.5
    BRAKING_CONST = 3.5

    speed = 0

    """This is actually the time "w" has been held for,
    but we decay it when "w" is not held so it can be analogous to RPM"""
    rpm = 0

    def __init__(self, texture: Texture, position: pygame.Vector2):
        super().__init__(texture, position)

    def movement(self, pressed_keys: list):
        # Update current speed
        self.speed = self._engine_power_curve(self.rpm)
        print(self.rpm)
        print(self.speed)

        if self.rpm > 5.5:
            self.rpm = 5.5
        elif self.rpm < -3:
            self.rpm = -3

        forward = pressed_keys[pygame.K_w]
        backwards = pressed_keys[pygame.K_s]
        left = pressed_keys[pygame.K_a]
        right = pressed_keys[pygame.K_d]

        if forward:
            # Braking
            if self.speed < 0:
                self.rpm += self.BRAKING_CONST * self.dt
            # Acceleration
            else:
                self.rpm += self.ACCELERATION_CONST * self.dt

        # Coasting
        if not forward and self.speed > 0:
            self.rpm -= self.COASTING_CONST * self.dt
        if not backwards and self.speed < 0:
            self.rpm += self.COASTING_CONST * self.dt

        if backwards:
            # Braking
            if self.speed > 0:
                self.rpm -= self.BRAKING_CONST * self.dt
            # Reversing
            else:
                self.rpm -= self.REVERSE_CONST * self.dt

        if left:
            self.texture.rotate(self.texture.angle - 5)
        if right:
            self.texture.rotate(self.texture.angle + 5)

        self.position = self._update_pos(
            self.position, self.dt, self.speed, self.texture.angle
        )

    def _engine_power_curve(self, rpm):
        if rpm > 5:
            return 600
        if rpm < -2:
            return -200
        else:
            return rpm * 120

    def _update_pos(self, current_pos: pygame.Vector2, dt, speed, heading: float):
        current_x = current_pos.x
        current_y = current_pos.y

        new_x = current_x + speed * dt * math.sin(math.radians(heading))
        new_y = current_y - speed * dt * math.cos(math.radians(heading))
        current_pos.update(new_x, new_y)

        return current_pos

    def draw(self, screen: pygame.Surface):
        """
        Draw the texture onto the given screen.
        Args:
            screen: The screen to draw to.
        """
        screen.blit(self.texture.texture, self.position)

        # end_x = self.position.x + 75 * math.sin(math.radians(self.texture.angle))
        # end_y = self.position.y - 75 * math.cos(math.radians(self.texture.angle))
        # end = pygame.Vector2(end_x, end_y)
        # pygame.draw.line(screen, "green", self.position, end, width=5)
