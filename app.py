import streamlit as st
import os
import json
import streamlit_lottie as st_lottie
from features.auth import authentication
from features.dashboard import user_dashboard

# Streamlit page configuration
st.set_page_config(
    page_title="Dost AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None
if 'user_data' not in st.session_state:
    st.session_state['user_data'] = {}

# Function for lottie file
def load_lottie_file(filepath: str):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

#################################### Introduction Page ####################################
def introduction():
    st.header("🤖DostAI: Your Mental Health Companion", divider='rainbow')
    with st.container(border=False):
        left_column, right_column = st.columns(2)
        with left_column:
            st.subheader("Welcome to DostAI!")
            intro_text = '''

            '''
            st.write(intro_text)
        with right_column:
            robot_file = load_lottie_file('animations/robot.json')
            st_lottie.st_lottie(robot_file, key='robot', height=450, width=450 ,loop=True)
        st.divider()

# Initialize session state for authentication
authentication()

# Page Navigation
if st.session_state["authentication_status"]:
    pg = st.navigation([
        st.Page(introduction, title='Introduction', icon='🙋🏻‍♂️'),
        st.Page("features/1-ChatBot.py", title='Share with Me (ChatBot)', icon='🤖'),
        st.Page("features/2-SymtomChecker.py", title='Symptom Checker', icon='🩺'),
        st.Page("features/3-DailyPlans.py", title='Daily Plans Maker', icon='📅'),
        st.Page("features/4-DailyReport.py", title='Daily Report', icon='📋'),
        st.Page(user_dashboard, title='Profile', icon='🧑🏻‍⚕️'),
    ])

    pg.run()