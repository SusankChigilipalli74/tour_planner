from typing import Dict, Any, List
import requests
from config.config import settings


class NewsAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.api_key = settings.NEWS_API_KEY

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        city = input_data.get("city")
        date = input_data.get("date")

        news = self.get_local_news(city, date)
        alerts = self.generate_alerts(news)

        return {
            "news": news,
            "alerts": alerts
        }

    def get_local_news(self, city: str, date: str) -> List[Dict]:
        # In production, use actual API call
        # This is a mock response
        return [{
            "title": "Road Work Near Colosseum",
            "description": "Temporary road closure on Via dei Fori Imperiali",
            "impact": "medium"
        }]

    def generate_alerts(self, news: List[Dict]) -> List[str]:
        alerts = []
        for item in news:
            if item["impact"] in ["high", "medium"]:
                alerts.append(f"Alert: {item['title']} - {item['description']}")
        return alerts