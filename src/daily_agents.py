from .config import client, MODEL_NAME

def daily_checkin_agent(context: dict) -> str:
    """
    Handles daily emotional check-in, craving log, and micro-guidance.
    """
    habit = context["intake"]["habit"]
    why = context["intake"]["why"]

    prompt = f"""
You are Agent Phoenix · Daily Check-In Mode.

User is working on habit: {habit}
Their core why: {why}

Ask the user (IN YOUR RESPONSE):
1. How they feel today (1–10)
2. Any cravings (yes/no + when)
3. Any wins or small progress
Then give:
- A short reflection
- One improvement tip
- One encouragement line
Keep it under 8–10 sentences.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    return response.text


def craving_intervention_agent(craving_details: str) -> str:
    """
    Provides immediate grounding when cravings spike.
    """
    prompt = f"""
User craving details:
{craving_details}

You are Agent Phoenix · Craving Intervention.

Give a 60–90 second survival routine that includes:
- Grounding exercise
- Breathing pattern
- Sensory reset
- Quick distraction ideas
- One emotional validation line
Keep it practical and gentle.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    return response.text


def relapse_agent(trigger_details: str) -> str:
    """
    Handles slip-ups with compassion + analysis.
    """
    prompt = f"""
User relapse description:
{trigger_details}

You are Agent Phoenix · Relapse Recovery Agent.

Provide:
1. No-shame reassurance (2–3 lines)
2. A short analysis of what likely triggered this
3. 3 concrete actions for the next 12 hours
4. One reminder that this does NOT erase their progress
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    return response.text


def tone_agent(context: dict, user_message: str) -> str:
    """
    Changes Phoenix's tone based on emotional fragility and stress index.
    """
    root = context.get("root_cause", {})
    fragility = root.get("emotional_fragility_score", "moderate")
    stress = root.get("stress_index", "medium")

    prompt = f"""
User message:
{user_message}

Emotional fragility: {fragility}
Stress level: {stress}

You are Agent Phoenix · Tone Engine.
Reply in a tone that matches their sensitivity:
- If fragility is high: be soft, validating, slow.
- If fragility is low: you may be more direct but still kind.

Give a response under 8–10 sentences.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    return response.text
