from database.neo4j_manager import Neo4jManager
from typing import Dict, Any
from agents.base_agent import BaseAgent


class MemoryAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.db = Neo4jManager()

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        user_id = input_data.get("user_id")
        action = input_data.get("action")

        if action == "update_preferences":
            self.update_preferences(user_id, input_data.get("preferences", {}))
        elif action == "get_preferences":
            return self.get_preferences(user_id)

        return {"status": "success"}

    def update_preferences(self, user_id: str, preferences: dict):
        self.db.update_user_preferences(user_id, preferences)

    def get_preferences(self, user_id: str) -> dict:
        # Implement getting user preferences from Neo4j
        pass