from datetime import datetime, timedelta
from typing import Dict, Any


def parse_time(time_str: str) -> datetime:
    """Convert time string to datetime object."""
    return datetime.strptime(time_str, "%H:%M")


def format_time(dt: datetime) -> str:
    """Convert datetime object to time string."""
    return dt.strftime("%H:%M")


def calculate_duration(start: str, end: str) -> int:
    """Calculate duration in minutes between two time strings."""
    start_time = parse_time(start)
    end_time = parse_time(end)
    duration = end_time - start_time
    return int(duration.total_seconds() / 60)


def format_currency(amount: float) -> str:
    """Format currency amount."""
    return f"${amount:.2f}"


def validate_itinerary(itinerary: Dict[str, Any]) -> bool:
    """Validate itinerary data."""
    required_fields = ["city", "date", "attractions"]
    return all(field in itinerary for field in required_fields)


def generate_time_slots(start_time: str, end_time: str,
                        slot_duration: int) -> List[Dict[str, str]]:
    """Generate time slots for itinerary."""
    slots = []
    current = parse_time(start_time)
    end = parse_time(end_time)

    while current < end:
        slot_end = current + timedelta(minutes=slot_duration)
        if slot_end > end:
            slot_end = end

        slots.append({
            "start": format_time(current),
            "end": format_time(slot_end)
        })

        current = slot_end

    return slots