import streamlit as st
import openai

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
        level = st.selectbox("Select your fitness level", ["beginner", "pro"], key='level')
        body_part = st.selectbox("Select the body part to focus on", ["upper body", "lower body", "core"], key='body_part')
        difficulty = st.selectbox("Select the difficulty level", ["easy", "medium", "hard"], key='difficulty')
        if st.button("Next"):
            st.session_state.step = 2

    if st.session_state.step == 2:
        goal = st.text_input("What is your specific fitness goal?", key='goal')
        equipment = st.text_input("What equipment do you have access to?", key='equipment')
        if st.button("Get Exercise Recommendation"):
            exercise = async.run(generate_exercise_recommendation(st.session_state.level, st.session_state.body_part, st.session_state.difficulty, goal, equipment))
            st.write(f"Recommended exercise for {st.session_state.level} level, focusing on {st.session_state.body_part}, with {st.session_state.difficulty} difficulty, aiming for {goal}, and using {equipment} is: {exercise}")

if __name__ == "__main__":
    app()
