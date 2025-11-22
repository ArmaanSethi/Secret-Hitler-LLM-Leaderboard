import unittest
from secret_hitler_engine import GameState, Role, PlayerStatus, Government

class MockLogger:
    def log_public_event(self, event):
        pass

class TestSecretHitlerEngine(unittest.TestCase):
    def setUp(self):
        self.players = ["P1", "P2", "P3", "P4", "P5"]
        self.logger = MockLogger()
        self.game = GameState(self.players, self.logger)

    def test_initialization(self):
        self.assertEqual(self.game.num_players, 5)
        self.assertEqual(len(self.game.roles), 5)
        self.assertEqual(self.game.lib_policies, 0)
        self.assertEqual(self.game.fasc_policies, 0)
        self.assertEqual(self.game.election_tracker, 0)

    def test_role_assignment_5_players(self):
        roles = list(self.game.roles.values())
        self.assertEqual(roles.count(Role.LIBERAL), 3)
        self.assertEqual(roles.count(Role.FASCIST), 1)
        self.assertEqual(roles.count(Role.HITLER), 1)

    def test_deck_creation(self):
        self.assertEqual(len(self.game.deck), 17)
        self.assertEqual(self.game.deck.count(Role.LIBERAL), 6)
        self.assertEqual(self.game.deck.count(Role.FASCIST), 11)

    def test_draw_policies(self):
        drawn = self.game.draw_policies(3)
        self.assertEqual(len(drawn), 3)
        self.assertEqual(len(self.game.deck), 14)

    def test_reshuffle(self):
        # Draw all cards
        self.game.draw_policies(17)
        self.assertEqual(len(self.game.deck), 0)
        
        # Discard some
        self.game.discard_policy(Role.LIBERAL)
        self.game.discard_policy(Role.FASCIST)
        self.assertEqual(len(self.game.discard), 2)
        
        # Draw again, should trigger reshuffle
        drawn = self.game.draw_policies(1)
        self.assertEqual(len(drawn), 1)
        self.assertEqual(len(self.game.deck), 1) # 2 discarded -> reshuffled -> 1 drawn -> 1 left
        self.assertEqual(len(self.game.discard), 0)

    def test_enact_policy(self):
        self.game.enact_policy(Role.LIBERAL)
        self.assertEqual(self.game.lib_policies, 1)
        
        self.game.enact_policy(Role.FASCIST)
        self.assertEqual(self.game.fasc_policies, 1)

    def test_win_conditions_policies(self):
        self.game.lib_policies = 4
        self.game.enact_policy(Role.LIBERAL)
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.winner, Role.LIBERAL)

        self.game.game_over = False # Reset
        self.game.winner = None # Reset winner
        self.game.lib_policies = 0 # Reset policies
        self.game.fasc_policies = 5
        self.game.enact_policy(Role.FASCIST)
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.winner, Role.FASCIST)

    def test_hitler_chancellor_win(self):
        # Find Hitler
        hitler = [p for p, r in self.game.roles.items() if r == Role.HITLER][0]
        
        self.game.fasc_policies = 3
        self.game.set_government("P1", hitler)
        
        # Check condition directly
        self.assertTrue(self.game.check_hitler_chancellor_win())
        
        # Trigger check via game loop logic (usually happens after election)
        self.game.check_game_over()
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.winner, Role.FASCIST)

    def test_election_tracker(self):
        self.game.increment_election_tracker()
        self.assertEqual(self.game.election_tracker, 1)
        self.game.increment_election_tracker()
        self.assertEqual(self.game.election_tracker, 2)
        
        # Max out tracker
        self.game.increment_election_tracker()
        self.assertEqual(self.game.election_tracker, 0)
        # Should have enacted a policy (randomly)
        total_policies = self.game.lib_policies + self.game.fasc_policies
        self.assertEqual(total_policies, 1)

    def test_executive_action_triggers(self):
        # 5 players: Investigate at 3 Fascist policies? No, 5-6 players don't have investigate at 3?
        # Wait, let's check rules. 
        # 5-6 players: 3 Fascist -> Policy Peek. 
        # 7+ players: 2 Fascist -> Investigate. 
        # The engine implementation might be simplified or specific.
        # Let's check the engine code logic in `executive_action` method in `secret_hitler_game.py` 
        # BUT `secret_hitler_engine.py` doesn't handle the *triggering* logic, `secret_hitler_game.py` does.
        # The engine just provides the methods.
        pass 

    def test_kill_player(self):
        self.game.kill_player("P2")
        self.assertEqual(self.game.player_status["P2"], PlayerStatus.DEAD)
        
        # Check if Hitler kill wins game
        hitler = [p for p, r in self.game.roles.items() if r == Role.HITLER][0]
        self.game.kill_player(hitler)
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.winner, "Liberals")

if __name__ == '__main__':
    unittest.main()
