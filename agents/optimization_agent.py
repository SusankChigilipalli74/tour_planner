from typing import Dict, Any, List
from .base_agent import BaseAgent


class OptimizationAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.transport_modes = {
            "walking": {"cost": 0, "speed": 4},  # km/h
            "taxi": {"cost": 2, "speed": 30},  # cost per km
            "bus": {"cost": 1.5, "speed": 20}  # fixed cost per ride
        }

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        itinerary = input_data.get("itinerary", [])
        budget = input_data.get("budget", 0)

        optimized_path = self.optimize_path(itinerary, budget)
        return {"optimized_path": optimized_path}

    def optimize_path(self, itinerary: List[Dict], budget: float) -> List[Dict]:
        optimized = []
        remaining_budget = budget

        for i in range(len(itinerary) - 1):
            current = itinerary[i]
            next_stop = itinerary[i + 1]

            # Calculate best transport mode based on distance and budget
            transport = self.get_best_transport(
                current, next_stop, remaining_budget
            )

            optimized.append({
                **current,
                "next_transport": transport
            })

            remaining_budget -= transport["cost"]

        # Add last stop
        if itinerary:
            optimized.append(itinerary[-1])

        return optimized

    def get_best_transport(self, current: Dict, next_stop: Dict, budget: float) -> Dict:
        distance = self.calculate_distance(current, next_stop)
        best_mode = "walking"
        best_cost = 0
        best_time = distance / self.transport_modes["walking"]["speed"]

        for mode, details in self.transport_modes.items():
            cost = details["cost"]
            if mode == "taxi":
                cost *= distance

            if cost <= budget:
                time = distance / details["speed"]
                if time < best_time:
                    best_mode = mode
                    best_cost = cost
                    best_time = time

        return {
            "mode": best_mode,
            "cost": best_cost,
            "time": round(best_time * 60)  # Convert to minutes
        }

    def calculate_distance(self, point1: Dict, point2: Dict) -> float:
        # Simplified distance calculation (would use actual coordinates in production)
        return 1.0  # Return dummy distance of 1km