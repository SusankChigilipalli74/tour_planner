from typing import Dict, Any
import requests
from config.config import settings


class WeatherAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.api_key = settings.WEATHER_API_KEY

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        city = input_data.get("city")
        date = input_data.get("date")

        weather_data = self.get_weather_forecast(city, date)
        recommendations = self.generate_recommendations(weather_data)

        return {
            "weather": weather_data,
            "recommendations": recommendations
        }

    def get_weather_forecast(self, city: str, date: str) -> Dict:
        # In production, use actual API call
        # This is a mock response
        return {
            "temperature": 22,
            "condition": "sunny",
            "precipitation_chance": 10,
            "wind_speed": 5
        }

    def generate_recommendations(self, weather_data: Dict) -> List[str]:
        recommendations = []

        if weather_data["condition"] == "sunny":
            recommendations.append("Bring sunscreen and sunglasses")
        elif weather_data["condition"] == "rainy":
            recommendations.append("Bring an umbrella")

        if weather_data["temperature"] < 15:
            recommendations.append("Bring a jacket")

        return recommendations