import unittest
import os
import json
from leaderboard_system import LeaderboardManager, EloCalculator

class TestLeaderboard(unittest.TestCase):
    def setUp(self):
        self.db_path = "test_leaderboard.db"
        self.lm = LeaderboardManager(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_elo_calculation(self):
        calc = EloCalculator(k_factor=32)
        # Equal rating, P1 wins
        winners = {"P1": 1200}
        losers = {"P2": 1200}
        new_winners, new_losers = calc.update_ratings(winners, losers)
        
        self.assertTrue(new_winners["P1"] > 1200)
        self.assertTrue(new_losers["P2"] < 1200)
        self.assertEqual(new_winners["P1"] + new_losers["P2"], 2400) # Zero sum check

    def test_record_match(self):
        match_data = {
            "winner": "Liberals",
            "players": {
                "Alice": "Liberal",
                "Bob": "Liberal",
                "Charlie": "Fascist",
                "Dave": "Hitler",
                "Eve": "Liberal"
            }
        }
        
        self.lm.record_match(match_data)
        
        # Check ratings
        alice_elo = self.lm.get_player_elo("Alice")
        charlie_elo = self.lm.get_player_elo("Charlie")
        
        self.assertTrue(alice_elo > 1200)
        self.assertTrue(charlie_elo < 1200)
        
        # Check stats
        players = self.lm.get_all_players()
        alice = next(p for p in players if p["name"] == "Alice")
        self.assertEqual(alice["matches_played"], 1)
        self.assertEqual(alice["wins"], 1)
        
        charlie = next(p for p in players if p["name"] == "Charlie")
        self.assertEqual(charlie["matches_played"], 1)
        self.assertEqual(charlie["losses"], 1)

if __name__ == '__main__':
    unittest.main()
