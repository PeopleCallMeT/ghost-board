# Ghost Board

> Multi-agent AI advisory board — where AI personas debate, challenge, and stress-test your ideas before you act on them.

---

## The Concept

**One sentence:** Instead of asking one AI to do everything, you build a team of AI specialists that debate each other—so you get answers that have already been stress-tested before they reach you.

**The analogy:** It's the difference between asking one consultant for advice versus watching a boardroom debate. You get the creative tension without paying for six salaries.

---

## How It Works

1. **User submits a problem** — "Should I pivot my business model?" or "How do I approach this negotiation?"

2. **The Board convenes** — Multiple AI agents, each with a distinct perspective, receive the problem

3. **They debate** — Visible to the user, agents challenge each other's assumptions, poke holes, build on ideas

4. **Synthesis** — An orchestrator agent synthesizes the debate into actionable recommendations

5. **Human in the loop** — User can jump in, redirect, ask follow-ups to any agent

---

## Architecture Components

| Component | Role |
|-----------|------|
| **Orchestrator** | Traffic cop — routes tasks, manages turns, synthesizes final output |
| **Agents** | Specialized personas with distinct system prompts |
| **Shared Memory** | Workspace where all agents can see the conversation |
| **Human Checkpoint** | User can watch, redirect, or intervene at any point |

---

## Framework: Six Thinking Hats + Personas

**Structure underneath:** Edward de Bono's Six Thinking Hats
**Personality on top:** Famous thinkers as personas

| Hat | Role | Persona Example |
|-----|------|-----------------|
| ⚪ White | Facts, data, research | The Researcher |
| ❤️ Red | Gut feel, intuition | The Gut Check |
| ⚫ Black | Risks, what could fail | Warren Buffett (The Skeptic) |
| 💛 Yellow | Benefits, what could work | Jeff Bezos (The Builder) |
| 💚 Green | Creativity, alternatives | Steve Jobs (The Simplifier) |
| 🔵 Blue | Process, synthesis | The Orchestrator |

Optional add: **Dalai Lama** as The Compass — ethics, human impact, "but should we?"

---

## Product Vision

**Build to sell.** Potential directions:

1. **DIY Platform** — Users build their own advisory board, pick personas, run problems through
2. **Vertical Solution** — Pre-built councils for specific use cases (M&A, marketing, product)
3. **White-Label** — Engine sold to consultants/agencies

---

## Tech Stack (TBD)

- Claude API for agents
- Orchestration layer (custom or Claude Agent SDK)
- Frontend to visualize the debate
- Shared memory (simple DB or in-memory)

---

## Project Status

- [ ] Define MVP scope
- [ ] Build agent system prompts
- [ ] Create orchestration logic
- [ ] Build visualization UI
- [ ] Test with real problems

