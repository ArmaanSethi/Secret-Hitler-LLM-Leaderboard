# Secret Hitler LLM Leaderboard Package
"""
A framework for evaluating Large Language Models on social deduction games.
"""

from .engine import GameState, Role, PlayerStatus
from .leaderboard import LeaderboardManager, EloCalculator
from .llm_clients import GoogleGenAIClient, OpenRouterClient, OllamaClient, MockClient
from .llm_interface import LLMPlayerInterface, GameLogger

__version__ = "1.0.0"
__all__ = [
    "GameState",
    "Role", 
    "PlayerStatus",
    "LeaderboardManager",
    "EloCalculator",
    "GoogleGenAIClient",
    "OpenRouterClient",
    "OllamaClient",
    "MockClient",
    "LLMPlayerInterface",
    "GameLogger",
]
