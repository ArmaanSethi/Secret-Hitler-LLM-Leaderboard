#!/usr/bin/env python3
"""
Entry point for running a Secret Hitler game.
Usage: python run.py 7 --log_to_file
"""
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from secret_hitler.game import GameConfig, GameRunner
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Play Secret Hitler with LLM players.")
    parser.add_argument("num_players", type=int,
                        help="Number of players (5-10)")
    parser.add_argument("--slowdown", type=int, default=0,
                        help="Slowdown timer in seconds (0 for no slowdown)")
    parser.add_argument("--press_enter", action="store_true",
                        help="Press enter to continue instead of timer")
    parser.add_argument("--debug_llm", action="store_true",
                        help="Enable LLM debug output")
    parser.add_argument("--log_to_file", action="store_true",
                        help="Enable logging to logs/ directory")
    parser.add_argument("--player_models", nargs="+",
                        help="Player configurations as JSON strings")
    args = parser.parse_args()

    if not 5 <= args.num_players <= 10:
        sys.exit("Players must be 5-10")
    if args.slowdown < 0:
        sys.exit("Slowdown must be non-negative")

    game_config = GameConfig(args)
    game_runner = GameRunner(game_config)

    start_msg = "Running Secret Hitler LLM Game."
    if game_config.slowdown_timer > 0:
        start_msg += f" Slowdown: {game_config.slowdown_timer}s."
    if game_config.debug_llm_enabled:
        start_msg += " Debug enabled."
    if game_config.log_to_file_enabled:
        start_msg += " Logging to logs/."
    print(start_msg)

    game_runner.run_game()


if __name__ == "__main__":
    main()
