import time
from .agents import (
    deep_intake_agent,
    root_cause_analysis_agent,
    plan_generation_agent,
)
from .daily_agents import (
    daily_checkin_agent,
    craving_intervention_agent,
    relapse_agent,
    tone_agent,
)
from .memory import load_memory, save_memory


def run_agent_phoenix_flow():
    print("\n=== Welcome to Agent Phoenix 🔥 ===\n")

    memory = load_memory()

    # ---------------- FIRST RUN: FULL INTAKE ----------------
    if not memory.get("completed_intake", False):
        print("[Agent Phoenix · Deep Intake] Let's understand you better.\n")

        context = {}
        deep_intake_agent(context)
        root_cause_analysis_agent(context)
        plan_generation_agent(context)

        memory["context"] = context
        memory["completed_intake"] = True
        save_memory(memory)

        print("\n🔥 Personalized plan created and saved!")
        print("Next time, Agent Phoenix will start in Daily Mode.\n")
        return

    # ---------------- DAILY MODE ----------------
    print("🔥 Daily Mode Activated — Agent Phoenix is with you.\n")

    context = memory["context"]

    while True:
        print("\nChoose an option:")
        print("1. Daily Check-In")
        print("2. I am having a craving")
        print("3. I relapsed")
        print("4. Talk to Phoenix (emotion support)")
        print("5. Exit")

        choice = input("\nEnter choice (1-5): ").strip()

        if choice == "1":
            response = daily_checkin_agent(context)
            print("\n📝 Daily Check-In:\n")
            print(response)

            memory.setdefault("checkins", []).append({
                "timestamp": time.time(),
                "response": response,
            })
            save_memory(memory)

        elif choice == "2":
            details = input("\nDescribe what you're feeling right now: ")
            response = craving_intervention_agent(details)
            print("\n🔥 Craving Intervention:\n")
            print(response)

            memory.setdefault("cravings", []).append({
                "timestamp": time.time(),
                "details": details,
            })
            save_memory(memory)

        elif choice == "3":
            details = input("\nTell me what happened: ")
            response = relapse_agent(details)
            print("\n🌱 Relapse Recovery:\n")
            print(response)

            memory.setdefault("relapses", []).append({
                "timestamp": time.time(),
                "details": details,
            })
            save_memory(memory)

        elif choice == "4":
            user_message = input("\nTell Phoenix what's on your mind: ")
            response = tone_agent(context, user_message)
            print("\n💬 Phoenix:\n")
            print(response)

        elif choice == "5":
            print("\n🔥 See you tomorrow, Agent. Stay strong.\n")
            break

        else:
            print("\nInvalid choice. Try again.")


if __name__ == "__main__":
    run_agent_phoenix_flow()
