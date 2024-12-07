# First, install required packages:
# pip install ollama requests

import streamlit as st
from datetime import datetime
import json
from utils.llm_helper import OllamaAPI


def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "user_data" not in st.session_state:
        st.session_state.user_data = {
            "city": None,
            "date": None,
            "time_range": None,
            "interests": [],
            "budget": None,
            "starting_point": None
        }
    if "stage" not in st.session_state:
        st.session_state.stage = "initial"
    if "llm" not in st.session_state:
        st.session_state.llm = OllamaAPI()


def process_message(message: str) -> str:
    llm = st.session_state.llm
    current_stage = st.session_state.stage
    user_data = st.session_state.user_data

    if current_stage == "initial":
        # Extract city from message
        cities = ["rome", "paris", "london", "new york", "tokyo"]
        mentioned_city = next((city for city in cities if city in message.lower()), None)

        if mentioned_city:
            user_data["city"] = mentioned_city
            st.session_state.stage = "time"
            return llm.generate_tour_response({"city": mentioned_city}, "greeting")

        return llm.generate_response(
            "The user wants to plan a trip but hasn't specified a city. Ask them which city they'd like to visit in a friendly way."
        )

    elif current_stage == "time":
        user_data["time_range"] = message
        st.session_state.stage = "interests"
        return llm.generate_tour_response(
            {"city": user_data["city"]},
            "interests"
        )

    elif current_stage == "interests":
        if "not sure" in message.lower():
            context = {
                "city": user_data["city"],
                "attractions": ["historical sites", "local cuisine", "art galleries"]
            }
            return llm.generate_tour_response(context, "suggestions")
        else:
            user_data["interests"] = [i.strip() for i in message.lower().split(",")]
            st.session_state.stage = "budget"
            return llm.generate_response(
                "Ask for their budget in a friendly way, mentioning that this will help customize their experience."
            )

    elif current_stage == "budget":
        try:
            budget = float(message.replace("$", "").strip())
            user_data["budget"] = budget
            st.session_state.stage = "starting_point"
            return llm.generate_response(
                "Ask where they'd like to start their tour from, mentioning they can provide a hotel or any specific location."
            )
        except ValueError:
            return "Could you please provide your budget as a number? For example: 150"

    elif current_stage == "starting_point":
        user_data["starting_point"] = message
        st.session_state.stage = "planning"

        context = {
            "city": user_data["city"],
            "budget": user_data["budget"],
            "interests": ", ".join(user_data["interests"]),
            "attractions": ["popular attractions based on interests"]
        }

        return llm.generate_tour_response(context, "itinerary")

    return llm.generate_response(
        "Ask how else you can help with their trip planning in a friendly way."
    )


def main():
    st.title("AI Tour Planning Assistant")
    init_session_state()

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Initial message
    if not st.session_state.messages:
        with st.chat_message("assistant"):
            initial_message = st.session_state.llm.generate_response(
                "Generate a friendly welcome message for a tour planning assistant, asking where they'd like to visit."
            )
            st.write(initial_message)
            st.session_state.messages.append({
                "role": "assistant",
                "content": initial_message
            })

    # Get user input
    if prompt := st.chat_input("Type here..."):
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Process and display response
        with st.chat_message("assistant"):
            response = process_message(prompt)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()