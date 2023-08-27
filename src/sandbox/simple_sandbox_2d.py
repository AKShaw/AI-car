import math
import os

import pygame


class SimpleSandbox2D:
    """
    2D sandbox with simple physics implemented in PyGame.

    Attributes:
        tps: Ticks per second. Defaults to 60.
        headless: If true, show no GUI. Defaults to false.
        resolution: Game window size.
    """

    # Attributes
    tps: int
    headless: bool
    resolution: list[int]

    # PyGame
    _screen: pygame.Surface
    _clock: pygame.time.Clock
    _running: bool = False

    # Textures
    _textures: dict[str, pygame.Surface] = {}

    _car_angle = 90

    def __init__(self, resolution, tps=60, headless=False):
        self.resolution = resolution
        self.tps = tps
        self.headless = headless

        # TODO: Controls with this
        if self.headless:
            os.environ["SDL_VIDEODRIVER"] = "dummy"

        pygame.init()
        self._screen = pygame.display.set_mode(self.resolution)
        self._clock = pygame.time.Clock()
        self._clock.tick(self.tps)
        pygame.display.set_caption("Simple 2D Car Sandbox")

        self._load_textures()

    def _load_textures(self):
        self._textures["car"] = pygame.image.load("src/resources/images/car.png")
        self._scale_texture("car", 0.2)

    def _scale_texture(self, texture_name: str, scale: float):
        """
        Scale a given texture by some proportion.
        Args:
            texture_name: the name of the texture to rescale.
            scale: The proportion to scale the texture by.

        Returns:
            The scaled texture.
        """
        texture = self._textures[texture_name]

        (current_height, current_width) = (texture.get_height(), texture.get_width())

        new_size = (current_width * scale, current_height * scale)
        self._textures[texture_name] = pygame.transform.smoothscale(texture, new_size)

    def _rotate_texture(self, texture_name: str, by_angle: float):
        texture = self._textures[texture_name]
        self._textures[texture_name] = pygame.transform.rotate(texture, by_angle)

    def start(self):
        self._running = True
        self._game_loop()

    def stop(self):
        self._running = False

    def _game_loop(self):
        # TODO: Refactor and make proper physics
        try:
            dt = 0
            player_pos = pygame.Vector2(
                self._screen.get_width() / 2, self._screen.get_height() / 2
            )

            while self._running:
                car_texture = self._textures["car"]

                # poll for events
                # pygame.QUIT event means the user clicked X to close your window
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.stop()

                # fill the screen with a color to wipe away anything from last frame
                self._screen.fill("white")

                self._screen.blit(car_texture, player_pos)

                keys = pygame.key.get_pressed()

                forward = keys[pygame.K_w]
                backwards = keys[pygame.K_s]
                left = keys[pygame.K_a]
                right = keys[pygame.K_d]

                if forward:
                    player_pos = self._update_pos(player_pos, dt, 300, self._car_angle)
                if backwards:
                    player_pos = self._update_pos(player_pos, dt, -300, self._car_angle)

                if left:
                    if forward:
                        self._rotate_texture("car", 5)
                        old_angle = self._car_angle
                        self._car_angle += 5
                        player_pos = self._update_pos(player_pos, dt, 300, old_angle)

                if right:
                    if forward:
                        self._rotate_texture("car", -5)
                        old_angle = self._car_angle
                        self._car_angle -= 5
                        player_pos = self._update_pos(player_pos, dt, 300, old_angle)

                # flip() the display to put your work on screen
                pygame.display.flip()

                dt = self._clock.tick(60) / 1000
        except KeyboardInterrupt:
            self.stop()

        pygame.quit()

    def _update_pos(self, current_pos: pygame.Vector2, dt, speed, old_angle):
        current_x = current_pos.x
        current_y = current_pos.y

        theta = old_angle - self._car_angle

        new_x = current_x + speed * dt * math.cos(theta)
        new_y = current_y + speed * dt * math.sin(theta)

        current_pos.update(new_x, new_y)

        return current_pos
