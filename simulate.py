#!/usr/bin/env python3
"""
Entry point for running simulations and updating the leaderboard.
Usage: python simulate.py --games 10 --players 7
"""
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from secret_hitler.simulation import SimulationRunner
import argparse


def main():
    parser = argparse.ArgumentParser(description="Run Secret Hitler Simulations")
    parser.add_argument("--games", type=int, default=1, 
                        help="Number of games to run")
    parser.add_argument("--players", type=int, default=7, 
                        help="Number of players per game")
    parser.add_argument("--workers", type=int, default=1, 
                        help="Number of parallel workers")
    parser.add_argument("--anonymous", action="store_true", 
                        help="Run with generic player names to prevent bias")
    parser.add_argument("--models", nargs="+", 
                        help="Player models config (optional)")

    args = parser.parse_args()

    runner = SimulationRunner(
        args.games, args.players, args.models, args.workers, args.anonymous
    )
    runner.run_simulations()


if __name__ == "__main__":
    main()
