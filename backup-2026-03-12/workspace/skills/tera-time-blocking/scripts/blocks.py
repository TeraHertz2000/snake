#!/usr/bin/env python3
"""
Convert minutes to 15-minute blocks and format a simple time-block row.
"""
import math
from datetime import datetime, timedelta

def blocks_from_minutes(minutes: int) -> int:
    return max(1, math.ceil(minutes / 15))

def add_blocks(start_iso: str, blocks: int) -> str:
    start = datetime.fromisoformat(start_iso)
    end = start + timedelta(minutes=blocks * 15)
    return end.isoformat(timespec="minutes")

def format_time_block(start_hour: int, start_minute: int, blocks: int, task: str, notes: str = "") -> str:
    """Format a time block row."""
    start = datetime(2026, 1, 1, start_hour, start_minute)
    end = start + timedelta(minutes=blocks * 15)
    start_str = start.strftime("%-H:%M")
    end_str = end.strftime("%-H:%M")
    
    lines = [
        f"{start_str} – {end_str} | [{blocks} block{'s' if blocks > 1 else ''}] {task}"
    ]
    if notes:
        lines.append(f"               | {notes}")
    return "\n".join(lines)

if __name__ == "__main__":
    # Example usage
    print("50 min →", blocks_from_minutes(50), "blocks")
    print(format_time_block(17, 0, 4, "Lifting session (Passion)", "Mousetrap: Change into gym clothes"))
