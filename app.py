import streamlit as st
import openai
import asyncio

from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=st.secrets["API_key"])

async def generate_exercise_recommendation(level, body_part, difficulty, goal, equipment):
    prompt_text = (
        f"I am a {level} fitness enthusiast looking to focus on my {body_part} with a {difficulty} difficulty level. "
        f"My specific goal is {goal} and I have access to {equipment}."
    )

    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a Gym instructor"},
            {"role": "user", "content": prompt_text}
        ],
    )

    return response.choices[0].message.content

def app():
    st.title("Fitness Exercise Recommendation App")

    if 'step' not in st.session_state:
        st.session_state.step = 1

    if st.session_state.step == 1:
        st.session_state.level = st.selectbox("Select your fitness level", ["beginner", "pro"])
        st.session_state.body_part = st.selectbox("Select the body part to focus on", ["upper body", "lower body", "core"])
        st.session_state.difficulty = st.selectbox("Select the difficulty level", ["easy", "medium", "hard"])
        if st.button("Next"):
            st.session_state.step = 2

    if st.session_state.step == 2:
        st.session_state.goal = st.text_input("What is your specific fitness goal?")
        st.session_state.equipment = st.text_input("What equipment do you have access to?")
        if st.button("Get Exercise Recommendation"):
            st.session_state.step = 3  # Proceed to show the recommendation
            st.experimental_rerun()

    if st.session_state.step == 3:
        if 'exercise' not in st.session_state:
            async def fetch_exercise():
                exercise = await generate_exercise_recommendation(
                    st.session_state.level,
                    st.session_state.body_part,
                    st.session_state.difficulty,
                    st.session_state.goal,
                    st.session_state.equipment
                )
                st.session_state.exercise = exercise
                st.experimental_rerun()

            asyncio.create_task(fetch_exercise())
            st.write("Fetching your exercise recommendation...")
        else:
            st.write(f"Recommended exercise for {st.session_state.level} level, focusing on {st.session_state.body_part}, with {st.session_state.difficulty} difficulty, aiming for {st.session_state.goal}, and using {st.session_state.equipment} is: {st.session_state.exercise}")
            if st.button("Start Over"):
                for key in ['step', 'level', 'body_part', 'difficulty', 'goal', 'equipment', 'exercise']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.experimental_rerun()

if __name__ == "__main__":
    app()
