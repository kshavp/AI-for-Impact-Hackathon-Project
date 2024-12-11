import streamlit as st
import os
import yaml
import json
from yaml.loader import SafeLoader
from streamlit_authenticator.utilities import Hasher
from streamlit_authenticator.utilities import LoginError
import streamlit_authenticator as stauth
import streamlit_lottie as st_lottie

# Streamlit page configuration
st.set_page_config(
    page_title="Dost AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Loading config file
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialize session state for register page
if 'register' not in st.session_state:
    st.session_state['register'] = False

def show_login_form():
    # Creating the authenticator object
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        # config['register_user']
    )
    
    # Creating a login widget
    try:
        authenticator.login()
    except LoginError as e:
        st.error(e)
    
    if st.session_state["authentication_status"]:
        authenticator.logout('Logout',"sidebar")
        st.sidebar.write(f'Welcome **{st.session_state["name"]}**👋')
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

    # Only show the "Register" button if the user is NOT logged in
    if st.session_state["authentication_status"] is None or st.session_state["authentication_status"] == False:
        st.write("---")
        if st.button("Register"):
            st.session_state['register'] = True  # Switch to register page

# Define function to show the register form
def show_register_form():
    with st.container():
        st.write("## Register")
        st.divider()
        new_username = st.text_input("Enter Username")
        new_name = st.text_input("Enter Your Full Name")
        new_password = st.text_input("Enter Password", type="password")
        new_email = st.text_input("Enter your email")
        preferred_lang = st.selectbox("Preferred Language", ["English", "Spanish", "French", "German", "Italian", "Portuguese", "Russian", "Chinese", "Japanese", "Korean"])

        if st.button("Submit Registration"):
            if new_username and new_password and new_email:
                # Hash the new password
                # hashed_password = Hasher().generate(new_password)[0]
                hashed_password = Hasher([new_password]).hash(new_password)
                if 'credentials' not in config:
                    config['credentials'] = {}
                if 'usernames' not in config['credentials']:
                    config['credentials']['usernames'] = {}
                    
                # Update the config dictionary
                config['credentials']['usernames'][new_username] = {
                    'name': new_name,
                    'password': hashed_password,
                    'email': new_email,
                    'preferred_lang': preferred_lang
                }
            
                # Save the updated credentials to the config.yaml file
                with open('config.yaml', 'w') as file:
                    yaml.dump(config, file)
                
                st.success("User registered successfully! You can now log in.")
            
            # Add a "Back to Login" button to return to the login page
    if st.button("Back to Login"):
        st.session_state['register'] = False  # Return to login page

preferred_lang = config['credentials']['usernames'][st.session_state['username']]['preferred_lang']

# Main section: Show either login or register form based on state
if st.session_state['register']:
    show_register_form()  # Show register form
else:
    show_login_form()  # Show login form

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



# Page Navigation
if st.session_state["authentication_status"]:
    pg = st.navigation([
        st.Page(introduction, title='Introduction', icon='🤖'),
        st.Page("features/1-ChatBot.py", title='Share with Me (ChatBot)', icon='🤖'),
        st.Page("features/2-SymtomChecker.py", title='Symptom Checker', icon='🩺'),
    ])

    pg.run()