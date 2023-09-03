import json
import math
import time
import tkinter
from abc import ABC
from pathlib import Path
from typing import List

import pygame as pg
import pygame.font

import tkinter.filedialog

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

    def behaviour(self, pressed_keys: list):
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

    def draw(self, surface: pg.Surface):
        super().draw(surface)
        font = pygame.font.SysFont(None, 24)
        speedometer = font.render(
            f"Speed: {self.speed:.2f}, RPM: {self.rpm:.2f}", True, "black"
        )
        turning = font.render(
            f"Max angle: {self._allowed_turning_angle(self.rpm):.2f}", True, "black"
        )
        surface.blit(speedometer, (10, 10))
        surface.blit(turning, (10, 36))

    def behaviour(self, pressed_keys: list):
        # Update current speed
        self.speed = self._engine_power_curve(self.rpm)

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
        angle = self._allowed_turning_angle(self.rpm)
        if self.speed < 0:
            angle *= -1
        if left:
            self.texture.rotate(self.texture.angle - angle)
        if right:
            self.texture.rotate(self.texture.angle + angle)

        self.position = self._update_pos(
            self.position, self.dt, self.speed, self.texture.angle
        )

    def _engine_power_curve(self, rpm):
        return rpm * 120

    def _allowed_turning_angle(self, rpm):
        rpm = abs(rpm)
        if rpm < 2.5:
            max_angle = rpm * 2
        elif rpm >= 2.5 and rpm < 7:
            max_angle = 5
        elif rpm >= 7:
            max_angle = -(rpm - 12)

        if max_angle < 0:
            max_angle = 0
        return max_angle

    def _update_pos(self, current_pos: pg.Vector2, dt, speed, heading: float):
        current_x = current_pos.x
        current_y = current_pos.y

        new_x = current_x + speed * dt * math.sin(math.radians(heading))
        new_y = current_y - speed * dt * math.cos(math.radians(heading))
        current_pos.update(new_x, new_y)

        return current_pos


class TrackBuilder(Entity):
    """
    Entity to provide track building functionality:
        - Saving, Loading, Drawing

    Attributes:
        track_path: The path to save/load the track to/from.
    """

    # TODO: Remove edges as we can infer these from points
    track_path: Path

    _desired_track_points: List[pg.Vector2]
    _desired_track_edges: List[List[pg.Vector2]]
    _finalised: bool

    def __init__(self, track_path):
        super().__init__(
            Texture("resources/images/transparent.png", 0, 1), pg.Vector2(0, 0)
        )
        self.track_path = track_path

        self._clear_track()
        self._finalised = False
        self._time_finalised_toggled = time.time()

    def draw(self, surface: pg.Surface):
        # Custom track drawing logic as this entity
        # doesn't have a texture
        if not self._finalised:
            for edge in self._desired_track_edges:
                pg.draw.line(surface, "red", edge[0], edge[1], 5)

            for point in self._desired_track_points:
                pg.draw.circle(surface, "green", point, 7, width=7)
        else:
            for edge in self._desired_track_edges:
                pg.draw.line(surface, "gray", edge[0], edge[1], 60)

            for point in self._desired_track_points:
                pg.draw.circle(surface, "gray", point, 30, width=60)

    def behaviour(self, pressed_keys: list):
        """
        Handles interaction.

        Args:
            pressed_keys:
                S: Save track
                L: Load track
                Delete: Clear track
                F: Finalise track, preview
                LMB: Draw track.

        """
        save_key_event = pressed_keys[pg.K_s]
        load_key_event = pressed_keys[pg.K_l]
        clear_track_key_event = pressed_keys[pg.K_DELETE]
        finalise_track_key_event = pressed_keys[pg.K_f]
        draw_desired_path_mouse_event = pg.mouse.get_pressed()[0]

        if save_key_event:
            self._save_track()

        if load_key_event:
            self._load_track()

        if clear_track_key_event:
            self._clear_track()

        if draw_desired_path_mouse_event:
            self._draw_track()

        if finalise_track_key_event:
            self._finalise_track()

    def _load_track(self):
        """
        Load the track data from self.track_path.
        Returns:
            None
        """
        self._clear_track()

        # Get load file
        top = tkinter.Tk()
        top.withdraw()
        file_name = tkinter.filedialog.askopenfilename(
            parent=top, title="Open Track", initialdir=self.track_path.absolute()
        )
        top.destroy()

        if file_name == "":
            return

        with open(file_name, "r") as track_file:
            data = json.load(track_file)

            for point in data["points"]:
                self._draw_track(pos=(point["x"], point["y"]))

    def _save_track(self):
        """
        Save the track data to self.track_path
        Returns:
            None
        Side effects:
            Writes a JSON file to self.track_path.
        """
        track_data = {"points": []}

        for point in self._desired_track_points:
            point_data = {
                "x": point.x,
                "y": point.y,
            }

            track_data["points"].append(point_data)

        # Get save file
        top = tkinter.Tk()
        top.withdraw()
        file_name = tkinter.filedialog.asksaveasfilename(
            parent=top, title="Save Track", initialdir=self.track_path.absolute()
        )
        top.destroy()

        if file_name == "":
            return

        with open(file_name, "w") as track_file:
            json.dump(track_data, track_file, indent=4)

    def _finalise_track(self):
        """
        Add the final edge to the track and change the draw mode.
        May be able to remove when edges gone.
        Returns:
            None
        """
        allow_toggle = False
        if (
            time.time() - self._time_finalised_toggled > 0.5
            and len(self._desired_track_points) >= 1
        ):
            allow_toggle = True
        if allow_toggle:
            self._finalised = not self._finalised
            self._time_finalised_toggled = time.time()

            if self._finalised:
                self._desired_track_edges.append(
                    [self._desired_track_points[-1], self._desired_track_points[0]]
                )
            else:
                del self._desired_track_edges[-1]

    def _draw_track(self, pos=None):
        """
        Handle drawing a new point on the track.
        Args:
            pos: The point to draw at. If none, use the mouse position.

        Returns:
            None
        """
        if pos is None:
            pos = pg.mouse.get_pos()

        previous_point = None
        if len(self._desired_track_points) > 1:
            previous_point = self._desired_track_points[-1]
        point = pg.Vector2(pos)
        self._desired_track_points.append(point)
        if previous_point is not None:
            edge = [previous_point, point]
            self._desired_track_edges.append(edge)

    def _clear_track(self):
        """
        Clear the track data.
        Returns:
            None
        """
        self._desired_track_points = []
        self._desired_track_edges = []
