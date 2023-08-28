import os

import pygame

from sandbox.simple_2d_sandbox.entities import Entity, Car
from sandbox.simple_2d_sandbox.textures import Texture


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

    _entities: list[Entity] = []

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

        self._load_entities()

    def _load_entities(self):
        self._entities.append(
            Car(
                Texture(
                    "resources/images/car.png",
                    display_angle=0,
                    scale=0.2,
                    pivot=pygame.Vector2(25, 70),
                ),
                # pygame.Vector2(0,0)
                pygame.Vector2(
                    self._screen.get_width() / 2, self._screen.get_height() / 2
                ),
            )
        )

    def start(self):
        self._running = True
        self._game_loop()

    def stop(self):
        self._running = False

    def _game_loop(self):
        # TODO: Refactor and make proper physics
        try:
            dt = 0

            while self._running:
                # poll for events
                # pygame.QUIT event means the user clicked X to close your window
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.stop()

                # fill the screen with a color to wipe away anything from last frame
                self._screen.fill("white")

                keys = pygame.key.get_pressed()
                for entity in self._entities:
                    entity.set_dt(dt)
                    entity.movement(keys)
                    entity.draw(self._screen)

                # flip() the display to put your work on screen
                pygame.display.flip()

                dt = self._clock.tick(60) / 1000
        except KeyboardInterrupt:
            self.stop()

        pygame.quit()
