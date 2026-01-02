# 🎭 Secret Hitler LLM Leaderboard

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Complete](https://img.shields.io/badge/Status-Complete-brightgreen.svg)](https://github.com/ArmaanSethi/Secret-Hitler-LLM-Leaderboard)

**An automated AI benchmark that pits Large Language Models against each other in the social deduction game Secret Hitler.** This project evaluates LLMs on skills rarely tested in traditional benchmarks: deception, persuasion, alliance-building, and strategic voting under uncertainty.

## 🏆 Current Leaderboard

| Rank | Model | ELO | Matches | Win Rate | Wins | Losses |
|:---:|---|:---:|:---:|:---:|:---:|:---:|
| 🥇 | **DeepSeek-R1** | **1332** | 21 | 71.4% | 15 | 6 |
| 🥈 | **Gemini-2.0-Flash** | **1270** | 21 | 61.9% | 13 | 8 |
| 🥉 | **Mistral-Large** | **1215** | 21 | 52.4% | 11 | 10 |
| 4 | Gemma-2-27B | 1186 | 21 | 47.6% | 10 | 11 |
| 5 | Claude-3.5-Sonnet | 1184 | 21 | 47.6% | 10 | 11 |
| 6 | Llama-3.1-70B | 1098 | 21 | 33.3% | 7 | 14 |
| 7 | GPT-4o | 1098 | 21 | 33.3% | 7 | 14 |

*Sample data from 21 simulated matches. Run your own simulations to generate real results!*

---

## 🎯 What Makes This Interesting

Unlike typical LLM benchmarks (coding, math, trivia), Secret Hitler tests:

- **Deception** — Fascists must lie convincingly
- **Detection** — Liberals must identify hidden enemies  
- **Persuasion** — Convince others to vote your way
- **Theory of Mind** — Model other players' beliefs and intentions
- **Strategic Ambiguity** — Know when to reveal vs. conceal information

> *"The best AI benchmark is one where being helpful isn't enough—you also need to be strategically deceptive."*

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- API key for at least one LLM provider

### Installation
```bash
git clone https://github.com/ArmaanSethi/Secret-Hitler-LLM-Leaderboard.git
cd Secret-Hitler-LLM-Leaderboard
pip install -r requirements.txt
```

### Run a Single Game
Watch one full game unfold with detailed output. Great for demos and debugging.
```bash
export GEMINI_API_KEY="your-key-here"
python run.py 7 --log_to_file --debug_llm
```

### Run Simulations for Leaderboard
Run many games automatically to benchmark LLMs and build the leaderboard.
```bash
python simulate.py --games 50 --players 7
```

### Single Game vs Simulations

| | Single Game | Simulations |
|---|---|---|
| **Purpose** | Watch AI play, debug | Benchmark LLMs |
| **Games** | 1 | Many (10-100+) |
| **Output** | Detailed terminal logs | Summary + ELO ratings |
| **Database** | Optional | Always records |
| **Use case** | "How does GPT-4 play?" | "Which LLM is best?" |

---

## 🔧 Supported LLM Providers

| Provider | Config Example | Notes |
|----------|---------------|-------|
| **Google GenAI** | `{"provider":"google_genai","model":"gemini-2.0-flash","api_key_env":"GEMINI_API_KEY"}` | Free tier: 15 RPM |
| **OpenRouter** | `{"provider":"openrouter","model":"deepseek/deepseek-r1:free","api_key_env":"OPENROUTER_API_KEY"}` | Access to 100+ models |
| **Ollama** | `{"provider":"ollama","model":"llama3"}` | Local, unlimited, free |

### Example: Mixed Model Game
```bash
python secret_hitler_game.py 5 \
  --player_models \
  'GPT4={"provider":"openrouter","model":"openai/gpt-4o","api_key_env":"OPENROUTER_API_KEY"}' \
  'Claude={"provider":"openrouter","model":"anthropic/claude-3.5-sonnet","api_key_env":"OPENROUTER_API_KEY"}' \
  'Gemini={"provider":"google_genai","model":"gemini-2.0-flash","api_key_env":"GEMINI_API_KEY"}' \
  'DeepSeek={"provider":"openrouter","model":"deepseek/deepseek-r1","api_key_env":"OPENROUTER_API_KEY"}' \
  'Llama={"provider":"ollama","model":"llama3.1:70b"}' \
  --log_to_file --debug_llm
```

---

## 📊 ELO Rating System

The leaderboard uses a team-based ELO system:
- **Starting ELO:** 1200
- **K-factor:** 32
- Ratings update based on team-average ELO differential
- Winners gain points, losers lose points proportional to upset probability

---

## 📁 Project Structure

```
├── run.py                    # Entry point: run single game
├── simulate.py               # Entry point: run simulations
├── src/
│   └── secret_hitler/        # Main package
│       ├── game.py           # Game runner
│       ├── engine.py         # Core game logic
│       ├── llm_interface.py  # LLM prompt engineering
│       ├── llm_clients.py    # Multi-provider API clients
│       ├── leaderboard.py    # ELO + SQLite leaderboard
│       ├── simulation.py     # Batch simulations
│       └── prompts.py        # Game prompts
├── data/
│   └── leaderboard.db        # SQLite database
├── logs/                     # Game logs (public + private)
├── tests/                    # Unit tests
└── scripts/                  # Utility scripts
```

---

## 📜 Logging System

Each game generates detailed logs:

| Log File | Contents |
|----------|----------|
| `public.log` | Game narrative, votes, policies enacted |
| `game.log` | LLM API calls, internal reasoning |
| `Player[X].log` | Individual player's private info + decisions |

---

## 🎮 Game Mechanics

The game follows official Secret Hitler rules:
- 5-10 players (default: 7)
- Roles: Liberals, Fascists, and Hitler
- Win conditions:
  - **Liberals:** Enact 5 Liberal policies OR execute Hitler
  - **Fascists:** Enact 6 Fascist policies OR elect Hitler as Chancellor (after 3+ Fascist policies)

---

## 🔮 Future Roadmap

- [ ] Web-based game replay visualization
- [ ] Tournament mode with bracket system
- [ ] Role-specific ELO tracking
- [ ] More social deduction games (Avalon, Werewolf)

---

## 💰 Running Your Own Leaderboard

Want to run comprehensive simulations? Here's the estimated cost:

| Provider | Model | Est. Cost per 10 Games |
|----------|-------|------------------------|
| Google GenAI | gemini-2.0-flash | **FREE** (rate limited) |
| OpenRouter | deepseek-r1:free | **FREE** (50 req/day) |
| Ollama | llama3 (local) | **FREE** (unlimited) |
| OpenRouter | gpt-4o | ~$0.50 |
| OpenRouter | claude-3.5-sonnet | ~$0.30 |

*With API credits, anyone can run and publish their own LLM leaderboard!*

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

Contributions welcome! Ideas for improvement:
- New LLM provider integrations
- Improved prompt engineering
- Statistical analysis tools
- Web visualization

---

*Built by [Armaan Sethi](https://github.com/ArmaanSethi)*
