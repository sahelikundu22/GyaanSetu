import streamlit as st
from database import init_db
from auth import signup, login

# Initialize database
init_db()

st.title("GyaanSetu")

# col1, col2 = st.columns(2)

# if col1.button("Sign Up"):
#     signup()

# if col2.button("Login"):
#     login()


# toggle
if "mode" not in st.session_state:
    st.session_state.mode = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if st.button(
    "Switch to Sign Up " if st.session_state.mode == "login" else "Switch to Login"
):
    if st.session_state.mode == "login":
        st.session_state.mode = "signup"
    else:
        st.session_state.mode = "login"
    st.rerun()


if st.session_state.mode == "signup":
    st.subheader("Sign Up")
    signup()
else:
    st.subheader("Login")
    login()


# Dashboard 
if "logged_in" in st.session_state and st.session_state.logged_in:
    st.write("### Dashboard")
    st.write("Name:", st.session_state.name)
    st.write("Email:", st.session_state.email)
    st.write("Points:", st.session_state.points)

    if st.button("Logout"):
        st.session_state.logged_in = False

