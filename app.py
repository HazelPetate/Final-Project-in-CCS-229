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

async def app():
    st.title("Fitness Exercise Recommendation App")

    level = st.selectbox("Select your fitness level", ["beginner", "pro"])
    body_part = st.selectbox("Select the body part to focus on", ["upper body", "lower body", "core"])
    difficulty = st.selectbox("Select the difficulty level", ["easy", "medium", "hard"])

    if st.button("Next"):
        goal = st.text_input("What is your specific fitness goal?")
        equipment = st.text_input("What equipment do you have access to?")
        
        if st.button("Get Exercise Recommendation"):
            exercise = await generate_exercise_recommendation(level, body_part, difficulty, goal, equipment)
            st.write(f"Recommended exercise for {level} level, focusing on {body_part}, with {difficulty} difficulty, aiming for {goal}, and using {equipment} is: {exercise}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(app())
