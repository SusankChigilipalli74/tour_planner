import requests
from typing import Dict, Any


class OllamaAPI:
    def __init__(self, model="llama3.2"):
        self.base_url = "http://localhost:11434/api"
        self.model = model

    def generate_response(self, prompt: str, system_prompt: str = None) -> str:
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        if system_prompt:
            data["system"] = system_prompt

        try:
            response = requests.post(f"{self.base_url}/generate", json=data)
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            print(f"Error calling Ollama: {e}")
            return "I apologize, but I'm having trouble generating a response right now."

    def generate_tour_response(self, context: Dict[str, Any], response_type: str) -> str:
        prompts = {
            "greeting": """
            You are a friendly and knowledgeable tour guide. The user wants to plan a trip to {city}.
            Generate a warm, welcoming response that asks about their travel dates and timing preferences.
            Keep the response conversational and encouraging.
            """,

            "interests": """
            As a tour guide familiar with {city}, generate a response that:
            1. Acknowledges their timing preferences
            2. Asks about their interests in a conversational way
            3. Mentions 2-3 popular categories of attractions in {city}
            Make it sound natural and enthusiastic.
            """,

            "itinerary": """
            Create a friendly, detailed response that:
            1. Presents an itinerary for {city}
            2. Includes their selected attractions: {attractions}
            3. Considers their budget of ${budget}
            4. Accounts for their interests in {interests}
            Make it sound like a real tour guide explaining a customized plan.
            Add personal touches and local insights.
            """,

            "restaurant": """
            As a local expert in {city}, recommend restaurants that:
            1. Match their cuisine preference: {cuisine}
            2. Fit their budget of ${budget}
            3. Are located near {location}
            Make it sound personal and include a brief description of why you recommend each place.
            """
        }

        prompt_template = prompts.get(response_type, "")
        prompt = prompt_template.format(**context)

        return self.generate_response(prompt)

