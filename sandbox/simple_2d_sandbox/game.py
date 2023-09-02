import os

import numpy as np
import pygame as pg
import pygame.font

from sandbox.simple_2d_sandbox.entities import Entity, Car
from sandbox.simple_2d_sandbox.textures import Texture


class SimpleSandbox2D:
    """
    2D sandbox with simple physics implemented in pg.

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
    _window: pg.Surface
    _clock: pg.time.Clock
    _running: bool = False

    _entities: list[Entity] = []

    def __init__(self, resolution, tps=60, headless=False):
        self.resolution = resolution
        self.tps = tps
        self.headless = headless

        # TODO: Controls with this
        if self.headless:
            os.environ["SDL_VIDEODRIVER"] = "dummy"

        pg.init()
        self._window = pg.display.set_mode(self.resolution)
        self._clock = pg.time.Clock()
        self._clock.tick(self.tps)
        pg.display.set_caption("Simple 2D Car Sandbox")

        self._load_entities()

    def _load_entities(self):
        self._entities.append(
            Car(
                Texture(
                    "resources/images/car.png",
                    display_angle=45,
                    scale=0.1,
                    pivot=pg.Vector2(25, 70),
                ),
                pg.Vector2(120, 900)
                # pg.Vector2(self._window.get_width() / 2, self._window.get_height() / 2),
            )
        )

    def start(self):
        self._running = True
        self._game_loop()

    def stop(self):
        self._running = False

    def _game_loop(self):
        try:
            dt = 1/self.tps
            screen_scale = list(np.array(self.resolution) / np.array([1920, 1080]))[0]

            while self._running:
                # poll for events
                # pg.QUIT event means the user clicked X to close your window
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.stop()

                # fill the screen with a color to wipe away anything from last frame
                self._window.blit(Texture("resources/images/spa.png",
                                          display_angle=0,
                                          scale=screen_scale,
                                          pivot=None).texture, (0, 0))

                font = pygame.font.SysFont(None, 24)
                fps_counter = font.render(f"FPS: {1/dt:.2f}", True, "black")
                self._window.blit(fps_counter, (self.resolution[0]-100, 10))

                keys = pg.key.get_pressed()
                for entity in self._entities:
                    entity.set_dt(dt)
                    entity.movement(keys)
                    entity.draw(self._window)

                # flip() the display to put your work on screen
                pg.display.flip()

                dt = self._clock.tick(60) / 1000
        except KeyboardInterrupt:
            self.stop()

        pg.quit()
