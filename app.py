import streamlit as st
import openai


from openai import AsyncOpenAI
from openai import OpenAI

client = AsyncOpenAI(
    # This is the default and can be omitted
    api_key=st.secrets["API_key"],
)
async def generate_exercise_recommendation(level, body_part, difficulty):
    prompt_text = (
        f"I am a {level} fitness enthusiast looking to focus on my {body_part} with a {difficulty} difficulty level. "
        f"Please recommend an appropriate exercise."
    )

    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt_text},
            {"role": "assistant", "content": "You are a Gym instructor"}
        ],
        
    )

    return response.choices[0].message.content


async def app():
    st.title("Fitness Exercise Recommendation App")

    level = st.selectbox("Select your fitness level", ["beginner", "pro"])
    body_part = st.selectbox("Select the body part to focus on", ["upper body", "lower body", "core"])
    difficulty = st.selectbox("Select the difficulty level", ["easy", "medium", "hard"])

    if st.button("Get Exercise Recommendation"):
        exercise = await generate_exercise_recommendation(level, body_part, difficulty)
        st.write(f"Recommended exercise for {level} level, focusing on {body_part}, with {difficulty} difficulty is: {exercise}")

#run the app
if __name__ == "__main__":
  import asyncio
  asyncio.run(app())
