import argparse
from sandbox.simple_2d_sandbox.game import SimpleSandbox2D


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
        default=[1280, 720],
        nargs=2,
        help="Sandbox window size (width, heigh) in pixels.",
    )

    return parser.parse_args()


def main():
    args = get_args()
    game = SimpleSandbox2D(args.resolution, tps=args.tps, headless=args.headless)
    game.start()


if __name__ == "__main__":
    main()
