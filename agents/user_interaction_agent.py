from typing import Dict, Any
from .base_agent import BaseAgent

class UserInteractionAgent(BaseAgent):
    def __init__(self, memory_agent):
        super().__init__()
        self.memory_agent = memory_agent
        self.required_info = [
            "city", "date", "start_time", "end_time",
            "interests", "budget", "starting_point"
        ]

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        missing_info = []
        collected_info = {}

        # Check for missing required information
        for info in self.required_info:
            if info not in input_data or not input_data[info]:
                missing_info.append(info)
            else:
                collected_info[info] = input_data[info]

        # Update user preferences in memory
        if collected_info:
            self.memory_agent.update_preferences(
                input_data["user_id"],
                collected_info
            )

        return {
            "missing_info": missing_info,
            "collected_info": collected_info
        }

    def generate_response(self, missing_info: list) -> str:
        if not missing_info:
            return "Great! I have all the information needed."

        questions = {
            "city": "Which city would you like to visit?",
            "date": "What date are you planning for?",
            "start_time": "What time would you like to start your day?",
            "end_time": "What time would you like to end your day?",
            "interests": "What are your interests? (e.g., history, food, shopping)",
            "budget": "What's your budget for the day?",
            "starting_point": "Where would you like to start your day?"
        }

        return questions[missing_info[0]]