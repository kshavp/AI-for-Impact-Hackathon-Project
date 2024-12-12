import streamlit as st
import google.generativeai as genai
from features.auth import get_user_details
from features.system_settings import  safety_settings, generation_config
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel(model_name="gemma-2-27b-it",
                safety_settings=safety_settings,
                generation_config=generation_config)

# Get user data from session state
user_data = get_user_details()

if not user_data:
    st.warning("You need to log in to create your daily report.")
    st.stop()

st.header("📋Daily Report", divider="rainbow")
with st.expander("What is Daily Report?"):
    st.write("Daily Report is a tool that uses Google Artificial Intelligence Model to help you generate a summary and advice based on your daily activities, feelings, and problems faced during the day. DostAI will help you to understand your day, feelings, tone, and activities.")

# Create a form for user input
with st.form("daily_report_form"):
    wake_up_time = st.time_input("When did you wake up?*")
    day_description = st.text_area("How was your day?*")
    day_rating = st.slider("Rate your day*", 1, 10)
    activities = st.text_area("What did you do today?*")
    problems = st.text_area("Did you face any problems or frustrations?*")
    feelings = st.text_area("How are you feeling?*")
    st.markdown("*Required**")
    submit_button = st.form_submit_button(label="Submit")

# Generate summary and advice based on user input
if submit_button:
    if not wake_up_time or not day_description or not day_rating or not activities or not problems or not feelings:
        st.error("Please fill out all the required fields.")
        st.stop()
    else:
        st.success("Your daily report has been submitted successfully.")

with st.spinner("Generating summary and advice..."):
    if wake_up_time and day_description and day_rating and activities and problems and feelings:    
        user_name = user_data.get('name', 'User')
        prompt = f"""
        User: {user_name}
        Wake up time: {wake_up_time}
        Day description: {day_description}
        Day rating: {day_rating}
        Activities: {activities}
        Problems: {problems}
        Feelings: {feelings}
        
        You are DostAI daily report generator. Understand the user's day, feelings, tone, and activities.
        
        Please provide a short summary of the user's day, give them greetings, and offer some advice based on their input.
        """
        response = model.generate_content(prompt)
        st.write(response.text)
    else:
        st.warning("Please fill out all the required fields to generate your daily report.")
