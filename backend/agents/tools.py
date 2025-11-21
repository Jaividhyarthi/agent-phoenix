from datetime import datetime
from typing import Dict, Any, List

from .memory import MemoryBank


def log_habit_checkin(
    memory: MemoryBank,
    user_id: str,
    habit_name: str,
    status: str,
    cravings_level: int,
    notes: str = "",
) -> Dict[str, Any]:
    """
    Tool to log a daily check-in for a habit.
    status: "success", "slip", "relapse"
    cravings_level: 0–10
    """
    entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "user_id": user_id,
        "habit_name": habit_name,
        "status": status,
        "cravings_level": cravings_level,
        "notes": notes,
    }
    memory.add_log(entry)
    return entry


def compute_habit_stats(memory: MemoryBank, habit_name: str) -> Dict[str, Any]:
    """
    Simple statistics tool over logs.
    """
    logs = memory.get_logs_for_habit(habit_name)
    total = len(logs)
    success = sum(1 for l in logs if l["status"] == "success")
    slips = sum(1 for l in logs if l["status"] == "slip")
    relapses = sum(1 for l in logs if l["status"] == "relapse")

    avg_craving = (
        sum(l["cravings_level"] for l in logs) / total if total > 0 else 0.0
    )

    return {
        "habit_name": habit_name,
        "total_days": total,
        "success_days": success,
        "slip_days": slips,
        "relapse_days": relapses,
        "success_rate": (success / total * 100.0) if total else 0.0,
        "avg_craving": avg_craving,
    }


def summarize_logs(memory: MemoryBank, habit_name: str) -> str:
    """
    Lightweight textual summary for last few entries that can be passed into Gemini.
    """
    logs = memory.get_logs_for_habit(habit_name)[-7:]  # last 7 entries
    lines: List[str] = []
    for l in logs:
        line = (
            f"{l['timestamp']} | {l['status'].upper()} | "
            f"craving={l['cravings_level']} | notes={l.get('notes','')}"
        )
        lines.append(line)
    if not lines:
        return "No logs yet for this habit."
    return "\n".join(lines)
