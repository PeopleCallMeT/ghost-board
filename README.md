# 👻 Ghost Board

**Your AI Advisory Board** — A team of legendary thinkers who debate your problems before you act.

> "Instead of asking one AI to do everything, you build a team of AI specialists that debate each other—so you get answers that have already been stress-tested before they reach you."

---

## The Board

| Agent | Persona | Core Question |
|-------|---------|---------------|
| 🔵 **Orchestrator** | Neutral moderator | "Where do we agree? Disagree?" |
| ⚫ **The Skeptic** | Warren Buffett | "What's the downside?" |
| 💛 **The Builder** | Jeff Bezos | "What does the customer want?" |
| 💚 **The Simplifier** | Steve Jobs | "What's the simplest version?" |
| 🧭 **The Compass** | Dalai Lama | "Who does this help or harm?" |

---

## Quick Start

### 1. Install dependencies

```bash
pip install anthropic
```

### 2. Set your API key

```bash
export ANTHROPIC_API_KEY=your_key_here
```

### 3. Run a session

```bash
cd /Users/tanyabeck/ghost-board
python ghost_board.py "Should I quit my job to start a business?"
```

---

## Example Session

```
🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮
           GHOST BOARD
    Your AI Advisory Board
🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮

📋 PROBLEM: Should I quit my job to start a business?

============================================================
🔵 THE ORCHESTRATOR
============================================================
[Frames the problem, identifies key dimensions]

============================================================
⚫ WARREN BUFFETT (The Skeptic)
============================================================
[Identifies risks, questions assumptions]

============================================================
💛 JEFF BEZOS (The Builder)
============================================================
[Pushes for action, asks about customers]

============================================================
💚 STEVE JOBS (The Simplifier)
============================================================
[Demands clarity and focus]

============================================================
🧭 DALAI LAMA (The Compass)
============================================================
[Asks about impact and motivation]

============================================================
🎯 FINAL SYNTHESIS
============================================================
[Recommendation, agreements, disagreements, next steps]
```

---

## Try These Problems

```bash
python ghost_board.py "Should I raise prices or add more features?"

python ghost_board.py "My cofounder and I disagree on strategy. How do we resolve it?"

python ghost_board.py "Should I take the safe corporate job or the risky startup offer?"

python ghost_board.py "How do I tell my biggest client I'm raising rates 50%?"
```

---

## Project Structure

```
ghost-board/
├── ghost_board.py          # Main CLI demo
├── README.md               # You are here
├── CLAUDE.md               # Project vision
├── architecture.md         # Technical architecture
└── agents/                 # Individual agent prompts
    ├── orchestrator.md
    ├── skeptic-buffett.md
    ├── builder-bezos.md
    ├── simplifier-jobs.md
    └── compass-dalailama.md
```

---

## What's Next

- [ ] Interactive mode (follow-up questions)
- [ ] Web UI to watch the debate visually
- [ ] Custom agent configuration
- [ ] Save/share sessions
- [ ] Add more personas (Munger, Brené Brown, Musk?)

---

## The Vision

**Build to sell.** This could become:

1. **DIY Platform** — Users build their own advisory boards
2. **Vertical Solution** — Pre-built councils for M&A, product, marketing
3. **White-Label** — Engine for consultants and agencies

---

*Built with Claude by Tanya Beck*
