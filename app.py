import streamlit as st


# Page Navigation
pg = st.navigation([
    st.Page("features/1-ChatBot.py", title='Chat with DostAI', icon='🤖'),
    st.Page("features/2-SymtomChecker.py", title='Symptom Checker', icon='🩺'),
])

pg.run()