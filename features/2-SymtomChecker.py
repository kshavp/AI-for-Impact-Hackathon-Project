import google.generativeai as genai
import streamlit as st
import time
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

st.header('Symptom Checker', anchor='symptom-checker', divider='rainbow')
st.write('This is a symptom checker tool that uses AI to help you identify possible health conditions based on your symptoms. And give the best possible advice on what to do next.')