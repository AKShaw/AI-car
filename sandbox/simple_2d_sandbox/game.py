import os
import argparse
from pathlib import Path

import pygame as pg
import pygame.font

from sandbox.simple_2d_sandbox.entities import Entity, Car, Track
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
    track_path: Path
    headless: bool
    resolution: list[int]

    # PyGame
    _window: pg.Surface
    _clock: pg.time.Clock
    _running: bool = False

    _entities: list[Entity] = []

    def __init__(self, resolution, track, tps=60, headless=False):
        self.resolution = resolution
        self.tps = tps
        self.headless = headless
        self.track_path = Path(track)

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
        track = Track(self.track_path)
        self._entities.append(track)

        self._entities.append(
            Car(
                Texture(
                    "resources/images/car.png",
                    display_angle=track.get_start_heading(),
                    scale=0.1,
                    pivot=pg.Vector2(25, 70),
                ),
                track.get_start_point(),
            )
        )

    def start(self):
        self._running = True
        self._game_loop()

    def stop(self):
        self._running = False

    def _game_loop(self):
        try:
            dt = 1 / self.tps

            while self._running:
                # poll for events
                # pg.QUIT event means the user clicked X to close your window
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.stop()

                # fill the screen with a color to wipe away anything from last frame
                self._window.fill("white")

                font = pygame.font.SysFont(None, 24)
                fps_counter = font.render(f"FPS: {1 / dt:.2f}", True, "black")
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
        "--headless",
        action="store_true",
        help="Launch the sandbox in headless mode (no GUI).",
    )
    parser.add_argument(
        "--resolution",
        type=int,
        default=[1920, 1080],
        nargs=2,
        help="Sandbox window size (width, heigh) in pixels.",
    )
    parser.add_argument(
        "--track",
        type=str,
        default="sandbox/simple_2d_sandbox/tracks/track1.json",
        help="Track file to play on.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    game = SimpleSandbox2D(
        args.resolution, args.track, tps=args.tps, headless=args.headless
    )
    game.start()
