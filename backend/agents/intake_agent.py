from google import genai
from .config import client, MODEL_NAME

# -------------- LLM CALL WRAPPER -----------------

def call_llm(prompt: str) -> str:
    """Simple wrapper to call Gemini using the new SDK."""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    return response.text


# -------------- AGENT 1: DEEP INTAKE -----------------

def deep_intake_agent(context: dict) -> dict:
    """
    Deep Intake Agent (Phase 2)
    Gathers: habit, why, timeline + 6 deep emotional/financial/environment questions.
    """

    print("\n[Agent Phoenix · Deep Intake] Let's understand you better.\n")

    habit = input("Name of the habit you want help with: ").strip()
    why = input("Why do you want to change this habit? (your 'why'): ").strip()
    timeline = input("Over how many days/weeks do you want to see progress?: ").strip()

    print("\n🔥 Great. Now I’ll ask a few deeper questions to understand your situation better.\n")

    emotional_state = input(
        "1. What emotions do you feel right before doing this habit? (e.g., lonely, stressed, bored): "
    ).strip()

    peak_trigger = input(
        "2. When was the last time you felt the strongest urge? What caused it?: "
    ).strip()

    environment = input(
        "3. Where are you usually when this habit happens the most? (home, college, work, outside): "
    ).strip()

    social_circle = input(
        "4. Do people around you also have this habit? (friends/family/colleagues): "
    ).strip()

    financial_context = input(
        "5. Does money play a role in why this habit continues? (yes/no + explanation): "
    ).strip()

    personal_story = input(
        "6. Tell me one moment that made you realize you want to change: "
    ).strip()

    context["intake"] = {
        "habit": habit,
        "why": why,
        "timeline": timeline,
        "emotional_state": emotional_state,
        "peak_trigger": peak_trigger,
        "environment": environment,
        "social_circle": social_circle,
        "financial_context": financial_context,
        "personal_story": personal_story,
    }

    print("\n🔥 Deep intake complete. Moving to root-cause analysis...\n")

    return context["intake"]


# -------------- AGENT 2: ROOT CAUSE ANALYSIS -----------------

def root_cause_analysis_agent(context: dict) -> dict:
    """
    Generates ULTRA-DEEP ROOT CAUSE ANALYSIS.
    """

    intake = context["intake"]

    prompt = f"""
You are Agent Phoenix's Root-Cause Analysis Agent.

Analyze the user's deep intake data and produce a ULTRA-DEEP psychological + behavioral root cause map.

INPUT DATA:
{intake}

OUTPUT STRICT JSON with these fields:
{{
  "emotional_root": "",
  "financial_root": "",
  "trauma_root": "",
  "relationship_root": "",
  "habit_loop": "",
  "dependency_level": "",
  "risk_level": "",
  "attachment_style": "",
  "coping_pattern": "",
  "relapse_likelihood": "",
  "trigger_categories": "",
  "self_worth_impact": "",
  "social_pressure_rating": "",
  "stress_index": "",
  "environment_safety_index": "",
  "mental_fatigue_level": "",
  "predicted_peak_craving_times": "",
  "suggested_agent_tone": "",
  "emotional_fragility_score": "",
  "financial_vulnerability_score": ""
}}
Make it accurate, structured, and NEVER include extra text outside JSON.
"""

    response_text = call_llm(prompt)

    import json, re

    raw = response_text.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()

    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        print("❌ Could not extract JSON. Response was:\n", raw)
        raise ValueError("Gemini did not return valid JSON")

    json_str = match.group()

    try:
        root_causes = json.loads(json_str)
    except json.JSONDecodeError:
        print("❌ JSON parse error:\n", json_str)
        raise

    context["root_cause"] = root_causes
    print("🔥 Root-cause analysis complete.\n")
    return root_causes


# -------------- AGENT 3: PLAN GENERATION -----------------

def plan_generation_agent(context: dict) -> dict:
    """
    Generates a 14-day personalized recovery plan.
    Uses both intake + root_cause from context.
    """

    intake = context["intake"]
    root = context["root_cause"]

    prompt = f"""
You are Agent Phoenix's Personalized Plan Agent.

Using the ULTRA-DEEP ROOT CAUSE ANALYSIS and user INTAKE, generate a
14-day adaptive recovery plan that considers:

- emotional root
- relationship triggers (ex-partner)
- trauma from breakup
- academic pressure
- stress index
- self-worth impact
- dependency level
- relapse likelihood
- predicted craving times
- emotional fragility score
- environmental triggers (college)
- social triggers (friends smoke)
- financial vulnerability (if relevant)
- suggested agent tone

FORMAT:
Return a structured dictionary with:

{{
  "summary": "",
  "daily_plan": [
      {{ "day": 1, "focus": "", "actions": [] }},
      {{ "day": 2, "focus": "", "actions": [] }}
  ],
  "emergency_protocol": [],
  "craving_replacement_kit": [],
  "emotional_support_script": "",
  "relapse_response_guide": "",
  "long_term_protection_plan": ""
}}

Make the plan realistic for a COLLEGE STUDENT with heartbreak triggers.
Do NOT include explanations outside the JSON.
"""

    response_text = call_llm(prompt)

    import json, re
    raw = response_text.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    match = re.search(r"\{.*\}", raw, re.DOTALL)

    if not match:
        print("❌ Plan JSON extraction failed:\n", raw)
        raise ValueError("Invalid plan JSON")

    plan = json.loads(match.group())
    context["plan"] = plan

    print("🔥 Personalized 14-day plan created.\n")
    return plan
