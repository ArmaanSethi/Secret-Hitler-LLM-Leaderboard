import sqlite3
import json
import os
from datetime import datetime
from collections import defaultdict

class EloCalculator:
    def __init__(self, k_factor=32, base_elo=1200):
        self.k_factor = k_factor
        self.base_elo = base_elo

    def calculate_expected_score(self, rating_a, rating_b):
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

    def update_ratings(self, winners, losers):
        """
        Updates ratings for a team game.
        winners: dict of {player_name: current_elo}
        losers: dict of {player_name: current_elo}
        """
        if not winners or not losers:
            return winners, losers

        avg_winner_elo = sum(winners.values()) / len(winners)
        avg_loser_elo = sum(losers.values()) / len(losers)

        expected_winner_score = self.calculate_expected_score(avg_winner_elo, avg_loser_elo)
        expected_loser_score = self.calculate_expected_score(avg_loser_elo, avg_winner_elo)

        # Actual scores: Winners get 1, Losers get 0
        new_winners = {}
        for player, elo in winners.items():
            change = self.k_factor * (1 - expected_winner_score)
            new_winners[player] = elo + change

        new_losers = {}
        for player, elo in losers.items():
            change = self.k_factor * (0 - expected_loser_score)
            new_losers[player] = elo + change

        return new_winners, new_losers

class LeaderboardManager:
    def __init__(self, db_path="leaderboard.db"):
        self.db_path = db_path
        self.elo_calc = EloCalculator()
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Players table
        c.execute('''CREATE TABLE IF NOT EXISTS players (
                     name TEXT PRIMARY KEY,
                     elo REAL,
                     matches_played INTEGER,
                     wins INTEGER,
                     losses INTEGER,
                     role_stats JSON
                     )''')

        # Matches table
        c.execute('''CREATE TABLE IF NOT EXISTS matches (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     timestamp TEXT,
                     winner_team TEXT,
                     details JSON
                     )''')
        
        conn.commit()
        conn.close()

    def get_player_elo(self, player_name):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT elo FROM players WHERE name=?", (player_name,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else self.elo_calc.base_elo

    def get_all_players(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM players ORDER BY elo DESC")
        players = []
        for row in c.fetchall():
            players.append({
                "name": row[0],
                "elo": row[1],
                "matches_played": row[2],
                "wins": row[3],
                "losses": row[4],
                "role_stats": json.loads(row[5]) if row[5] else {}
            })
        conn.close()
        return players

    def record_match(self, match_data):
        """
        match_data should contain:
        - winner: "Liberals" or "Fascists"
        - players: dict of {player_name: role}
        - log_path: str (optional)
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        winner_team = match_data["winner"]
        players_roles = match_data["players"]
        
        # 1. Identify winners and losers
        winners = {}
        losers = {}
        
        for player, role in players_roles.items():
            current_elo = self.get_player_elo(player)
            
            # Determine if player won
            is_winner = False
            # Role.LIBERAL.value is "Liberal", Role.FASCIST.value is "FASCIST"
            if winner_team == "Liberal" and role == "Liberal":
                is_winner = True
            elif winner_team == "FASCIST" and role in ("FASCIST", "Hitler"):
                is_winner = True
                
            if is_winner:
                winners[player] = current_elo
            else:
                losers[player] = current_elo

        # 2. Calculate new ELOs
        new_winners, new_losers = self.elo_calc.update_ratings(winners, losers)
        
        # 3. Update Database
        all_updates = {**new_winners, **new_losers}
        
        for player, new_elo in all_updates.items():
            # Get existing stats
            c.execute("SELECT matches_played, wins, losses, role_stats FROM players WHERE name=?", (player,))
            row = c.fetchone()
            
            if row:
                matches_played, wins, losses, role_stats_json = row
                role_stats = json.loads(role_stats_json) if role_stats_json else {}
            else:
                matches_played = 0
                wins = 0
                losses = 0
                role_stats = {}
            
            matches_played += 1
            is_win = player in new_winners
            if is_win:
                wins += 1
            else:
                losses += 1
                
            # Update role stats
            role = players_roles[player]
            if role not in role_stats:
                role_stats[role] = {"played": 0, "won": 0}
            role_stats[role]["played"] += 1
            if is_win:
                role_stats[role]["won"] += 1
                
            c.execute('''INSERT OR REPLACE INTO players 
                         (name, elo, matches_played, wins, losses, role_stats) 
                         VALUES (?, ?, ?, ?, ?, ?)''',
                      (player, new_elo, matches_played, wins, losses, json.dumps(role_stats)))

        # 4. Record Match
        c.execute("INSERT INTO matches (timestamp, winner_team, details) VALUES (?, ?, ?)",
                  (timestamp, winner_team, json.dumps(match_data)))
        
        conn.commit()
        conn.close()
        return new_winners, new_losers

if __name__ == "__main__":
    # Simple test
    lm = LeaderboardManager()
    print("Leaderboard initialized.")
    print("Current players:", lm.get_all_players())
