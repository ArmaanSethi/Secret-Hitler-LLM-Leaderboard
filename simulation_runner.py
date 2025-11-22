import argparse
import json
import os
import time
import concurrent.futures
from secret_hitler_game import GameConfig, GameRunner
from leaderboard_system import LeaderboardManager

class SimulationRunner:
    def __init__(self, num_games, num_players, player_models, max_workers=1):
        self.num_games = num_games
        self.num_players = num_players
        self.player_models = player_models
        self.max_workers = max_workers
        self.leaderboard = LeaderboardManager()

    def run_single_game(self, game_id):
        print(f"Starting Game {game_id}...")
        
        # Construct arguments for GameConfig
        # We need to mock the args object expected by GameConfig
        class MockArgs:
            def __init__(self, num_players, player_models):
                self.num_players = num_players
                self.slowdown = 0
                self.press_enter = False
                self.debug_llm = False
                self.log_to_file = True # Always log for simulations
                self.player_models = player_models

        # Prepare player models argument
        # We need to assign models to players dynamically or use the provided list
        # For now, let's assume player_models is a list of config strings like "Player1={...}"
        # If not provided, we use a default set.
        
        current_player_models = []
        if self.player_models:
             current_player_models = self.player_models
        else:
            # Default to a mix if not specified, or just use the default in GameConfig
            # Let's construct a default set using a free model for testing
            default_model_config = {
                "provider": "openrouter",
                "model": "google/gemini-2.0-flash-lite-preview-02-05:free",
                "api_key_env": "OPENROUTER_API_KEY"
            }
            for i in range(self.num_players):
                current_player_models.append(f"Player{i+1}={json.dumps(default_model_config)}")

        args = MockArgs(self.num_players, current_player_models)
        
        try:
            config = GameConfig(args)
            runner = GameRunner(config)
            
            # We need to modify GameRunner to return the result instead of just printing it
            # Since we can't easily modify the running instance method without changing the class,
            # we will rely on the game state after run_game() returns.
            # BUT run_game() has a loop that breaks on game over.
            
            # Let's capture the game state after execution
            runner.setup_game()
            
            # Run the game loop manually here to avoid sys.exit or infinite loops if any
            # Copying logic from runner.run_game() but adapted
            
            game_state = runner.game_state
            
            while not game_state.check_game_over():
                gov_approved = runner.election_phase()

                if gov_approved:
                    game_state.election_tracker = 0
                    if game_state.check_hitler_chancellor_win():
                        game_state.game_over = True
                        game_state.winner = "Fascists"
                        break
                    enacted_policy = runner.legislative_session()
                    if enacted_policy:
                        runner.executive_action()
                else:
                    game_state.reset_government()
                    game_state.increment_election_tracker()
                    if game_state.election_tracker >= 3:
                        game_state.enact_chaos_policy()
                        game_state.election_tracker = 0
                        if game_state.game_over:
                            break

                if not game_state.check_game_over():
                    game_state.next_president()
            
            # Game Over
            print(f"Game {game_id} Finished. Winner: {game_state.winner}")
            
            # Record result
            winner_str = game_state.winner.value if hasattr(game_state.winner, 'value') else str(game_state.winner)
            match_data = {
                "winner": winner_str,
                "players": {p: game_state.roles[p].value if hasattr(game_state.roles[p], 'value') else str(game_state.roles[p]) for p in game_state.players},
                "game_id": game_id
            }
            
            self.leaderboard.record_match(match_data)
            return match_data

        except Exception as e:
            print(f"Error in Game {game_id}: {e}")
            import traceback
            traceback.print_exc()
            return None

    def run_simulations(self):
        print(f"Starting simulation of {self.num_games} games with {self.max_workers} workers.")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(self.run_single_game, i+1) for i in range(self.num_games)]
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    print(f"Match recorded: {result['winner']} won.")

        print("All simulations complete.")
        self.print_leaderboard()

    def print_leaderboard(self):
        players = self.leaderboard.get_all_players()
        print("\n=== LEADERBOARD ===")
        print(f"{'Rank':<5} {'Name':<15} {'ELO':<10} {'Matches':<10} {'Win Rate':<10}")
        print("-" * 60)
        for i, p in enumerate(players):
            win_rate = (p['wins'] / p['matches_played'] * 100) if p['matches_played'] > 0 else 0
            print(f"{i+1:<5} {p['name']:<15} {p['elo']:<10.1f} {p['matches_played']:<10} {win_rate:<10.1f}%")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Secret Hitler Simulations")
    parser.add_argument("--games", type=int, default=1, help="Number of games to run")
    parser.add_argument("--players", type=int, default=7, help="Number of players per game")
    parser.add_argument("--workers", type=int, default=1, help="Number of parallel workers")
    parser.add_argument("--models", nargs="+", help="Player models config (optional)")
    
    args = parser.parse_args()
    
    runner = SimulationRunner(args.games, args.players, args.models, args.workers)
    runner.run_simulations()
