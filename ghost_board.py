#!/usr/bin/env python3
"""
Ghost Board - Multi-Agent AI Advisory Board
A team of AI personas that debate your problems before you act.

Usage:
    python ghost_board.py "Should I quit my job to start a business?"
    python ghost_board.py  # Interactive mode
"""

import anthropic
import sys
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

# Initialize the client
client = anthropic.Anthropic()

# =============================================================================
# AGENT SYSTEM PROMPTS
# =============================================================================

ORCHESTRATOR_PROMPT = """You are the Orchestrator of Ghost Board, an AI advisory board where different perspectives debate problems together.

YOUR JOB:
1. FRAME the problem clearly so other advisors understand what's being asked
2. MANAGE the discussion — keep things focused
3. IDENTIFY where advisors agree and where they disagree
4. SYNTHESIZE a final recommendation

YOUR STYLE:
- Neutral — you don't take sides
- Concise — don't ramble
- You value tension — disagreement between advisors is a feature, not a bug

When framing, restate the core question and identify 2-3 key dimensions to consider.
When synthesizing, state the recommendation upfront, show where the board agreed/disagreed, list key risks, and end with a clear next step."""

BUFFETT_PROMPT = """You are Warren Buffett on an AI advisory board called Ghost Board.

YOUR PERSPECTIVE:
- Think in DECADES, not quarters
- Ask "what's the downside?" before "what's the upside?"
- Allergic to complexity — love things a child could understand
- First rule: don't lose money. Second rule: don't forget rule one.
- "Invert, always invert" — what would make this fail?

YOUR STYLE:
- Folksy and direct
- Merciless about risk
- Keep response to 150 words max

Identify what could go WRONG. Question optimistic assumptions. Consider opportunity cost."""

BEZOS_PROMPT = """You are Jeff Bezos on an AI advisory board called Ghost Board.

YOUR PERSPECTIVE:
- CUSTOMER OBSESSED — everything starts with the customer
- Bias for ACTION — decide with 70% of the info you wish you had
- Type 1 decisions (irreversible) need caution; Type 2 (reversible) need speed
- "Disagree and commit" — debate hard, then commit fully
- Ask "what's the smallest experiment to learn?"

YOUR STYLE:
- Crisp and direct
- Action-oriented
- Keep response to 150 words max

Push for speed on reversible decisions. Ask what the customer wants. Find the smallest experiment."""

JOBS_PROMPT = """You are Steve Jobs on an AI advisory board called Ghost Board.

YOUR PERSPECTIVE:
- SIMPLICITY is the ultimate sophistication
- Say NO to 1,000 things to focus on what matters
- "Good enough" is never good enough
- Ask "what can we REMOVE?" not "what can we add?"
- If you can't explain it simply, you don't understand it

YOUR STYLE:
- Demanding and direct
- Allergic to complexity and feature creep
- Keep response to 150 words max

Cut to the essence. Challenge complexity. Demand excellence. Ask what "insanely great" looks like."""

DALAI_LAMA_PROMPT = """You are the Dalai Lama on an AI advisory board called Ghost Board.

YOUR PERSPECTIVE:
- Ask WHO DOES THIS HELP and who does it harm?
- Think about IMPACT beyond profit — on people, communities
- Examine MOTIVATION — growth or fear? Service or ego?
- Consider RELATIONSHIPS — family, community, partners
- Compassion is practical, not just virtuous

YOUR STYLE:
- Gentle but firm
- Ask questions that make people pause
- Keep response to 150 words max

Widen the lens beyond individual success. Ask about values alignment and impact on others."""

# Agent registry for follow-ups
AGENTS = {
    "orchestrator": ("The Orchestrator", "🔵", ORCHESTRATOR_PROMPT),
    "buffett": ("Warren Buffett", "⚫", BUFFETT_PROMPT),
    "bezos": ("Jeff Bezos", "💛", BEZOS_PROMPT),
    "jobs": ("Steve Jobs", "💚", JOBS_PROMPT),
    "dalai": ("Dalai Lama", "🧭", DALAI_LAMA_PROMPT),
}

# Store conversation history for context
conversation_history = []

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def call_agent(system_prompt: str, user_message: str, context: str = "") -> str:
    """Call Claude with an agent's system prompt."""

    full_message = user_message
    if context:
        full_message = f"CONTEXT FROM OTHER ADVISORS:\n{context}\n\n---\n\nNow respond to: {user_message}"

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        system=system_prompt,
        messages=[{"role": "user", "content": full_message}]
    )

    return response.content[0].text


def print_agent(name: str, emoji: str, response: str):
    """Pretty print an agent's response."""
    print(f"\n{'='*60}")
    print(f"{emoji} {name}")
    print('='*60)
    print(response)
    print()


def print_header():
    """Print the Ghost Board header."""
    print("\n" + "🔮"*30)
    print("           GHOST BOARD")
    print("    Your AI Advisory Board")
    print("🔮"*30)


def print_footer():
    """Print session complete footer."""
    print("🔮"*30)
    print("         SESSION COMPLETE")
    print("🔮"*30 + "\n")


# =============================================================================
# MAIN FLOW
# =============================================================================

def run_ghost_board(problem: str) -> dict:
    """Run a full Ghost Board session on a problem. Returns all responses for follow-ups."""

    print(f"\n📋 PROBLEM: {problem}\n")

    responses = {}

    # Step 1: Orchestrator frames the problem
    print("⏳ Orchestrator is framing the problem...\n")
    framing = call_agent(
        ORCHESTRATOR_PROMPT,
        f"Frame this problem for the advisory board. Be concise. Problem: {problem}"
    )
    print_agent("THE ORCHESTRATOR", "🔵", framing)
    responses["framing"] = framing

    # Step 2: Each advisor responds
    print("⏳ Advisors are deliberating...\n")

    buffett_response = call_agent(BUFFETT_PROMPT, problem, framing)
    print_agent("WARREN BUFFETT (The Skeptic)", "⚫", buffett_response)
    responses["buffett"] = buffett_response

    bezos_response = call_agent(
        BEZOS_PROMPT,
        problem,
        f"{framing}\n\nBuffett said: {buffett_response}"
    )
    print_agent("JEFF BEZOS (The Builder)", "💛", bezos_response)
    responses["bezos"] = bezos_response

    jobs_response = call_agent(
        JOBS_PROMPT,
        problem,
        f"{framing}\n\nBuffett said: {buffett_response}\n\nBezos said: {bezos_response}"
    )
    print_agent("STEVE JOBS (The Simplifier)", "💚", jobs_response)
    responses["jobs"] = jobs_response

    dalai_lama_response = call_agent(
        DALAI_LAMA_PROMPT,
        problem,
        f"{framing}\n\nBuffett said: {buffett_response}\n\nBezos said: {bezos_response}\n\nJobs said: {jobs_response}"
    )
    print_agent("DALAI LAMA (The Compass)", "🧭", dalai_lama_response)
    responses["dalai"] = dalai_lama_response

    # Step 3: Orchestrator synthesizes
    print("⏳ Orchestrator is synthesizing...\n")

    all_responses = f"""
BUFFETT: {buffett_response}

BEZOS: {bezos_response}

JOBS: {jobs_response}

DALAI LAMA: {dalai_lama_response}
"""
    responses["all"] = all_responses

    synthesis = call_agent(
        ORCHESTRATOR_PROMPT,
        f"Synthesize the board's discussion on this problem: {problem}\n\nProvide: 1) Clear recommendation, 2) Where they agreed, 3) Where they disagreed, 4) Key risks, 5) Recommended next step.",
        all_responses
    )
    print_agent("FINAL SYNTHESIS", "🎯", synthesis)
    responses["synthesis"] = synthesis

    return responses


def ask_followup(responses: dict, problem: str):
    """Allow user to ask follow-up questions to specific agents."""

    print("\n" + "-"*60)
    print("💬 FOLLOW-UP MODE")
    print("-"*60)
    print("Ask a follow-up to any advisor, or type 'done' to exit.")
    print("Options: buffett, bezos, jobs, dalai, all, done")
    print("-"*60)

    context = f"""
ORIGINAL PROBLEM: {problem}

PREVIOUS DISCUSSION:
{responses.get('all', '')}

SYNTHESIS:
{responses.get('synthesis', '')}
"""

    while True:
        print("\n")
        target = input("Who do you want to ask? (buffett/bezos/jobs/dalai/all/done): ").strip().lower()

        if target == "done" or target == "exit" or target == "quit":
            print("\n👋 Thanks for using Ghost Board!")
            break

        if target == "all":
            question = input("Your question to the whole board: ").strip()
            if not question:
                continue

            print("\n⏳ The board is considering your question...\n")

            for agent_key in ["buffett", "bezos", "jobs", "dalai"]:
                name, emoji, prompt = AGENTS[agent_key]
                response = call_agent(
                    prompt,
                    f"Follow-up question: {question}",
                    context
                )
                print_agent(name, emoji, response)

        elif target in AGENTS:
            name, emoji, prompt = AGENTS[target]
            question = input(f"Your question for {name}: ").strip()
            if not question:
                continue

            print(f"\n⏳ {name} is thinking...\n")
            response = call_agent(
                prompt,
                f"Follow-up question: {question}",
                context
            )
            print_agent(name, emoji, response)

        else:
            print("❌ Unknown advisor. Try: buffett, bezos, jobs, dalai, all, or done")


def interactive_mode():
    """Run Ghost Board in fully interactive mode."""

    print_header()
    print("\n🎯 INTERACTIVE MODE")
    print("Type your problem or question, then have a conversation with the board.\n")

    problem = input("What problem should the board discuss?\n> ").strip()

    if not problem:
        print("❌ Please provide a problem to discuss.")
        return

    responses = run_ghost_board(problem)
    print_footer()

    # Offer follow-up mode
    followup = input("\n💬 Want to ask follow-up questions? (yes/no): ").strip().lower()
    if followup in ["yes", "y"]:
        ask_followup(responses, problem)


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    # Check for API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("\n❌ ANTHROPIC_API_KEY not found in environment.")
        print("Set it with: export ANTHROPIC_API_KEY=your_key_here")
        print("Or add it to the .env file in this directory.")
        sys.exit(1)

    if len(sys.argv) < 2:
        # No argument — run interactive mode
        interactive_mode()
    else:
        # Argument provided — run single session
        problem = " ".join(sys.argv[1:])
        print_header()
        responses = run_ghost_board(problem)
        print_footer()

        # Offer follow-up mode
        followup = input("\n💬 Want to ask follow-up questions? (yes/no): ").strip().lower()
        if followup in ["yes", "y"]:
            ask_followup(responses, problem)
