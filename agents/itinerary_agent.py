from typing import Dict, Any, List
from .base_agent import BaseAgent

class ItineraryAgent(BaseAgent):
    def __init__(self, memory_agent):
        super().__init__()
        self.memory_agent = memory_agent
        self.attractions = {
            "Rome": {
                "historical": [
                    {"name": "Colosseum", "duration": 90, "fee": 15, "status": "Open"},
                    {"name": "Roman Forum", "duration": 75, "fee": 12, "status": "Open"},
                    {"name": "Pantheon", "duration": 45, "fee": 0, "status": "Open"}
                ],
                "food": [
                    {"name": "Piazza Navona", "duration": 60, "fee": 0, "status": "Open"},
                    {"name": "Indian Affair Rome", "duration": 40, "fee": 20, "status": "Open"}
                ],
                "relaxation": [
                    {"name": "Trevi Fountain", "duration": 45, "fee": 0, "status": "Open"},
                    {"name": "Spanish Steps", "duration": 45, "fee": 0, "status": "Open"}
                ]
            }
            # Add more cities here
        }

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        city = input_data.get("city")
        interests = input_data.get("interests", [])
        budget = input_data.get("budget", 0)
        start_time = input_data.get("start_time")
        end_time = input_data.get("end_time")

        # Generate itinerary based on interests and budget
        itinerary = self.generate_itinerary(city, interests, budget, start_time, end_time)
        return {"itinerary": itinerary}

    def generate_itinerary(self, city: str, interests: List[str], budget: float,
                          start_time: str, end_time: str) -> List[Dict]:
        selected_attractions = []
        remaining_budget = budget
        current_time = self.parse_time(start_time)
        end_time = self.parse_time(end_time)

        # Select attractions based on interests and budget
        for interest in interests:
            if interest in self.attractions[city]:
                for attraction in self.attractions[city][interest]:
                    if remaining_budget >= attraction["fee"]:
                        if current_time + attraction["duration"] <= end_time:
                            selected_attractions.append({
                                **attraction,
                                "start_time": self.format_time(current_time),
                                "end_time": self.format_time(current_time + attraction["duration"])
                            })
                            current_time += attraction["duration"] + 15  # 15 min buffer
                            remaining_budget -= attraction["fee"]

        return selected_attractions

    def parse_time(self, time_str: str) -> int:
        # Convert time string (HH:MM) to minutes since start of day
        hours, minutes = map(int, time_str.split(":"))
        return hours * 60 + minutes

    def format_time(self, minutes: int) -> str:
        # Convert minutes since start of day to time string (HH:MM)
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours:02d}:{mins:02d}"