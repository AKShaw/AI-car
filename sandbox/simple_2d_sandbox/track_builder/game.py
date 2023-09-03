import argparse
from pathlib import Path

import numpy as np
import pygame as pg
import pygame.font

from sandbox.simple_2d_sandbox.entities import Entity, TrackBuilder


class SimpleSandbox2DTrackBuilder:
    """
    2D sandbox track builder

    Attributes:
        tps: Ticks per second. Defaults to 60.
        headless: If true, show no GUI. Defaults to false.
        resolution: Game window size.
    """

    # Attributes
    tps: int
    resolution: list[int]
    save_location: Path

    # PyGame
    _window: pg.Surface
    _clock: pg.time.Clock
    _running: bool = False

    _entities: list[Entity] = []

    def __init__(self, resolution, save_locatiom, tps=60):
        self.resolution = resolution
        self.tps = tps
        self.save_location = save_locatiom

        pg.init()
        self._window = pg.display.set_mode(self.resolution)
        self._clock = pg.time.Clock()
        self._clock.tick(self.tps)
        pg.display.set_caption("Simple 2D Track Builder")

        self._load_entities()

    def _load_entities(self):
        self._entities.append(TrackBuilder(self.save_location))

    def start(self):
        self._running = True
        self._game_loop()

    def stop(self):
        self._running = False

    def _game_loop(self):
        try:
            dt = 1 / self.tps
            screen_scale = list(np.array(self.resolution) / np.array([1920, 1080]))[0]

            while self._running:
                # poll for events
                # pg.QUIT event means the user clicked X to close your window
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.stop()

                # fill the screen with a color to wipe away anything from last frame
                self._window.fill("white")

                font = pygame.font.SysFont(None, 24)
                fps_counter = font.render(f"FPS: {1/dt:.2f}", True, "black")
                self._window.blit(fps_counter, (self.resolution[0] - 100, 10))

                keys = pg.key.get_pressed()
                for entity in self._entities:
                    entity.set_dt(dt)
                    entity.behaviour(keys)
                    entity.draw(self._window)

                # flip() the display to put your work on screen
                pg.display.flip()

                dt = self._clock.tick(60) / 1000
        except KeyboardInterrupt:
            self.stop()

        pg.quit()


def get_args():
    parser = argparse.ArgumentParser(prog="AI Car Sandbox.")

    parser.add_argument("--tps", type=int, default=60, help="Ticks per second.")
    parser.add_argument(
        "--resolution",
        type=int,
        default=[1920, 1080],
        nargs=2,
        help="Sandbox window size (width, heigh) in pixels.",
    )
    parser.add_argument(
        "--save-path",
        type=str,
        default="tracks/default.json",
        help="Save location for the designed track.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    game = SimpleSandbox2DTrackBuilder(
        args.resolution, Path(args.save_path), tps=args.tps
    )
    game.start()
