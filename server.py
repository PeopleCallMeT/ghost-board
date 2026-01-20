#!/usr/bin/env python3
"""
Ghost Board Web Server
Serves the web UI and handles API requests for debates.
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='ui')
CORS(app)

client = anthropic.Anthropic()

# =============================================================================
# AGENT PROMPTS
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

AGENTS = {
    "orchestrator": {"name": "The Orchestrator", "emoji": "🔵", "prompt": ORCHESTRATOR_PROMPT, "role": "Moderator"},
    "buffett": {"name": "Warren Buffett", "emoji": "⚫", "prompt": BUFFETT_PROMPT, "role": "The Skeptic"},
    "bezos": {"name": "Jeff Bezos", "emoji": "💛", "prompt": BEZOS_PROMPT, "role": "The Builder"},
    "jobs": {"name": "Steve Jobs", "emoji": "💚", "prompt": JOBS_PROMPT, "role": "The Simplifier"},
    "dalai": {"name": "Dalai Lama", "emoji": "🧭", "prompt": DALAI_LAMA_PROMPT, "role": "The Compass"},
}

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

# =============================================================================
# ROUTES
# =============================================================================

@app.route('/')
def index():
    return send_from_directory('ui', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('ui', path)

@app.route('/api/agents', methods=['GET'])
def get_agents():
    """Return list of available agents."""
    return jsonify({
        key: {
            "name": agent["name"],
            "emoji": agent["emoji"],
            "role": agent["role"]
        }
        for key, agent in AGENTS.items()
    })

@app.route('/api/frame', methods=['POST'])
def frame_problem():
    """Have orchestrator frame the problem."""
    data = request.json
    problem = data.get('problem', '')

    if not problem:
        return jsonify({"error": "No problem provided"}), 400

    response = call_agent(
        ORCHESTRATOR_PROMPT,
        f"Frame this problem for the advisory board. Be concise. Problem: {problem}"
    )

    return jsonify({
        "agent": "orchestrator",
        "name": "The Orchestrator",
        "emoji": "🔵",
        "role": "Moderator",
        "response": response
    })

@app.route('/api/advise', methods=['POST'])
def get_advice():
    """Get advice from a specific agent."""
    data = request.json
    problem = data.get('problem', '')
    agent_key = data.get('agent', '')
    context = data.get('context', '')

    if not problem or not agent_key:
        return jsonify({"error": "Missing problem or agent"}), 400

    if agent_key not in AGENTS:
        return jsonify({"error": f"Unknown agent: {agent_key}"}), 400

    agent = AGENTS[agent_key]
    response = call_agent(agent["prompt"], problem, context)

    return jsonify({
        "agent": agent_key,
        "name": agent["name"],
        "emoji": agent["emoji"],
        "role": agent["role"],
        "response": response
    })

@app.route('/api/synthesize', methods=['POST'])
def synthesize():
    """Have orchestrator synthesize the discussion."""
    data = request.json
    problem = data.get('problem', '')
    responses = data.get('responses', '')

    if not problem:
        return jsonify({"error": "No problem provided"}), 400

    response = call_agent(
        ORCHESTRATOR_PROMPT,
        f"Synthesize the board's discussion on this problem: {problem}\n\nProvide: 1) Clear recommendation, 2) Where they agreed, 3) Where they disagreed, 4) Key risks, 5) Recommended next step.",
        responses
    )

    return jsonify({
        "agent": "synthesis",
        "name": "Final Synthesis",
        "emoji": "🎯",
        "role": "Recommendation",
        "response": response
    })

@app.route('/api/followup', methods=['POST'])
def followup():
    """Ask a follow-up question to a specific agent."""
    data = request.json
    question = data.get('question', '')
    agent_key = data.get('agent', '')
    context = data.get('context', '')

    if not question or not agent_key:
        return jsonify({"error": "Missing question or agent"}), 400

    if agent_key not in AGENTS:
        return jsonify({"error": f"Unknown agent: {agent_key}"}), 400

    agent = AGENTS[agent_key]
    response = call_agent(agent["prompt"], f"Follow-up question: {question}", context)

    return jsonify({
        "agent": agent_key,
        "name": agent["name"],
        "emoji": agent["emoji"],
        "role": agent["role"],
        "response": response
    })

# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("\n❌ ANTHROPIC_API_KEY not found. Add it to .env file.")
        exit(1)

    print("\n🔮 Ghost Board Server starting...")
    print("   Open http://localhost:5001 in your browser\n")
    app.run(debug=True, port=5001)
