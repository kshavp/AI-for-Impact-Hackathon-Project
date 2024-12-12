import streamlit as st
from features.auth import get_user_details

def user_dashboard():
    user_data = get_user_details()
    name = user_data.get('name', 'N/A')

    if not user_data:
        st.warning("You need to log in to view your dashboard.")
        return

    st.header("🧑🏻‍⚕️User Dashboard", divider="rainbow")
    st.subheader(f"Welcome {name}, Here is your information:")

    with st.container(border=True):
        st.subheader("Personal Information", divider="rainbow")
        st.write(f"**Name:** {user_data.get('name', 'N/A')}")
        st.write(f"**Email:** {user_data.get('email', 'N/A')}")
        st.write(f"**Age:** {user_data.get('age', 'N/A')}")
        st.write(f"**Gender:** {user_data.get('gender', 'N/A')}")
        st.write(f"**Preferred Language:** {user_data.get('preferred_lang', 'N/A')}")

    with st.container(border=True):
        st.subheader("Professional Information", divider="rainbow")
        st.write(f"**Designation:** {user_data.get('designation', 'N/A')}")
        st.write(f"**Working Hours:** {user_data.get('working_hours', 'N/A')}")
        st.write(f"**Working Place:** {user_data.get('working_place', 'N/A')}")
        st.write(f"**Problem Facing:** {user_data.get('prob_facing', 'N/A')}")
        st.write(f"**Problem Reason:** {user_data.get('prob_reason', 'N/A')}")
        st.write(f"**Status:** {user_data.get('status', 'N/A')}")

if __name__ == "__main__":
    user_dashboard()