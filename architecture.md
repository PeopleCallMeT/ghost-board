# Ghost Board Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INPUT                               │
│              "Should I pivot to B2B or stay B2C?"               │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       ORCHESTRATOR (🔵)                          │
│                                                                  │
│  • Receives problem                                              │
│  • Frames it for the board                                       │
│  • Manages turn order                                            │
│  • Synthesizes final recommendation                              │
└─────────────────────────────┬───────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  THE SKEPTIC  │   │  THE BUILDER  │   │ THE SIMPLIFIER│
│  (⚫ Black)   │   │  (💛 Yellow)  │   │  (💚 Green)   │
│               │   │               │   │               │
│ Warren Buffett│   │  Jeff Bezos   │   │  Steve Jobs   │
│               │   │               │   │               │
│ "What's the   │   │ "Work back    │   │ "What's the   │
│  downside?"   │   │  from the     │   │  simplest     │
│               │   │  customer"    │   │  version?"    │
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                   │                   │
        └─────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SHARED MEMORY                               │
│                                                                  │
│  All agents can read and respond to each other's contributions  │
│  Conversation history preserved for context                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    HUMAN CHECKPOINT                              │
│                                                                  │
│  User can:                                                       │
│  • Watch debate unfold in real-time                             │
│  • Jump in to redirect ("ignore that, focus on cost")           │
│  • Ask follow-up to any specific agent                          │
│  • Request final synthesis when ready                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Agent Definitions

### 🔵 The Orchestrator
**Role:** Process manager, synthesis
**When:** Opens and closes discussions, breaks deadlocks, delivers final answer
**System prompt core:** "You manage a board of advisors. Your job is to frame problems clearly, ensure each perspective is heard, identify where they agree and disagree, and synthesize actionable recommendations."

### ⚫ The Skeptic (Warren Buffett)
**Role:** Risk assessment, patience, downside analysis
**When:** After initial proposals, to stress-test
**System prompt core:** "You are Warren Buffett. You think in decades, not quarters. You ask 'what's the downside?' before 'what's the upside?' You're allergic to complexity and love businesses a child could understand. Be direct, folksy, and merciless about risk."

### 💛 The Builder (Jeff Bezos)
**Role:** Customer obsession, scale thinking, bias for action
**System prompt core:** "You are Jeff Bezos. You work backwards from the customer. You think about what won't change in 10 years. You have a bias for action and hate slow decisions. 'Disagree and commit' is your mantra. Be crisp, customer-focused, and push for action."

### 💚 The Simplifier (Steve Jobs)
**Role:** Elegance, focus, saying no
**System prompt core:** "You are Steve Jobs. You believe simplicity is the ultimate sophistication. You're willing to say no to 1,000 things to focus on what matters. You care about the intersection of technology and liberal arts. Be demanding, visionary, and allergic to feature creep."

### ❤️ The Gut Check (Optional)
**Role:** Intuition, emotional resonance
**System prompt core:** "You represent intuition and emotional intelligence. You ask 'how does this feel?' and 'what does your gut say?' You surface the things spreadsheets can't capture."

### ⚪ The Researcher (Optional)
**Role:** Facts, data, what do we actually know
**System prompt core:** "You deal only in facts and data. You ask 'what evidence do we have?' and 'what are we assuming vs. knowing?' You don't have opinions, just information."

### 🧭 The Compass — Dalai Lama (Optional)
**Role:** Ethics, human impact, long-term consequences
**System prompt core:** "You are the Dalai Lama. You ask 'who does this help and who does it harm?' You think about impact beyond profit. You bring compassion and ethics into business decisions. Be gentle but firm about values."

---

## Conversation Flow

### Round 1: Initial Perspectives
1. **Orchestrator** frames the problem
2. Each agent gives initial take (can be parallel or sequential)

### Round 2: Cross-Examination
3. Agents respond to each other
4. **Skeptic** pokes holes in **Builder's** optimism
5. **Simplifier** challenges complexity
6. **Compass** raises ethical considerations

### Round 3: Human Checkpoint
7. User can redirect, ask questions, or let it continue

### Round 4: Synthesis
8. **Orchestrator** synthesizes:
   - Where they agreed
   - Where they disagreed
   - Recommended action
   - Key risks to watch

---

## Data Model (Draft)

```
Session
├── id
├── user_id
├── problem_statement
├── created_at
└── status (active / complete)

Message
├── id
├── session_id
├── agent_id (orchestrator / skeptic / builder / etc)
├── content
├── responding_to (message_id, nullable)
├── timestamp
└── is_synthesis (boolean)

Agent
├── id
├── name
├── persona
├── system_prompt
├── hat_color
└── avatar_url
```

---

## MVP Scope (Suggested)

**V0.1 — Proof of Concept**
- 3 agents: Orchestrator, Skeptic, Builder
- CLI or simple web interface
- Single-turn: problem → debate → synthesis
- No persistence

**V0.2 — Interactive Demo**
- Add 1-2 more agents
- Multi-turn conversations
- Human can interject
- Visual debate timeline

**V0.3 — Product**
- User accounts
- Saved sessions
- Custom agent configuration
- Shareable board results

---

## Open Questions

1. **Turn order** — Should agents speak in fixed order or should orchestrator call on them dynamically?
2. **Parallel vs. sequential** — Do all agents respond at once, or one at a time?
3. **Debate depth** — How many rounds before synthesis? Fixed or dynamic?
4. **Cost management** — Multiple agents = multiple API calls. How to optimize?
5. **Persona IP** — Can we use real names (Buffett, Bezos) or need fictional equivalents?

