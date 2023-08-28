import math
from abc import ABC

import pygame as pg

from sandbox.simple_2d_sandbox.textures import Texture


class Entity(ABC):
    texture: Texture
    position: pg.Vector2

    dt: int  # Time since last tick (for frame rate independant physics)

    def __init__(self, texture: Texture, position: pg.Vector2):
        self.texture = texture
        self.position = position

    def draw(self, surface: pg.Surface):
        """
        Draw the texture onto the given surface.
        Args:
            surface: The surface to draw to.
        """
        self.texture.draw(surface, self.position)

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
    ACCELERATION_CONST = 3
    REVERSE_CONST = 1
    COASTING_CONST = 0.5
    BRAKING_CONST = 4

    speed = 0

    """This is actually the time "w" has been held for,
    but we decay it when "w" is not held so it can be analogous to RPM"""
    rpm = 0

    def __init__(self, texture: Texture, position: pg.Vector2):
        super().__init__(texture, position)

    def movement(self, pressed_keys: list):
        # Update current speed
        self.speed = self._engine_power_curve(self.rpm)

        # print(f"RPM: {self.rpm:.2f}")

        if self.rpm > 10:
            self.rpm = 10
        elif self.rpm < -3:
            self.rpm = -3

        forward = pressed_keys[pg.K_w]
        backwards = pressed_keys[pg.K_s]
        left = pressed_keys[pg.K_a]
        right = pressed_keys[pg.K_d]

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

        # Steering
        if left:
            angle = self._allowed_turning_angle(self.rpm)
            self.texture.rotate(self.texture.angle - angle)
        if right:
            angle = self._allowed_turning_angle(self.rpm)
            self.texture.rotate(self.texture.angle + angle)

        self.position = self._update_pos(
            self.position, self.dt, self.speed, self.texture.angle
        )

    def _engine_power_curve(self, rpm):
        return rpm * 120

    def _allowed_turning_angle(self, rpm):
        # max_angle = -math.log(abs(rpm))**2+5
        max_angle = 0

        # TODO: Find better settings
        rpm = abs(rpm)
        if rpm < 2:
            max_angle = rpm*1.5
        elif rpm > 6:
            max_angle = rpm*0.8
        else:
            max_angle = rpm*1

        if max_angle < 0:
            max_angle = 0
        print(f"Max angle: {max_angle:.2f}")
        return max_angle


    def _update_pos(self, current_pos: pg.Vector2, dt, speed, heading: float):
        current_x = current_pos.x
        current_y = current_pos.y

        new_x = current_x + speed * dt * math.sin(math.radians(heading))
        new_y = current_y - speed * dt * math.cos(math.radians(heading))
        current_pos.update(new_x, new_y)

        return current_pos
