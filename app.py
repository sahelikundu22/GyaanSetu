import streamlit as st
from database import init_db
from auth import signup, login, auth_dialog

st.set_page_config(
    page_title="GyaanSetu",
    page_icon="📚",
    layout="wide"
)

# Initialize database
init_db()

# st.title("GyaanSetu")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# MAIN UI
if not st.session_state.logged_in:
    # Not registered view
    
    st.markdown(
        "<h1 style='text-align:center;'>GyaanSetu</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h4 style='text-align:center; color:gray;'>Connecting Ambition with Education</h4>",
        unsafe_allow_html=True
    )
    
    st.divider()
    

    # YOUTUBE INPUT
    youtube_url = st.text_input(
        "🔗 Enter YouTube URL",
        placeholder="https://www.youtube.com/watch?v=..."
    )

    if st.button("Generate Transcript"):
        if youtube_url:
            st.write("Processing:", youtube_url)
            # fn call
        else:
            st.warning("Please enter a YouTube URL")

    st.divider()


    st.markdown("""
        <h3> Generic resources only take you so far. By creating your GyaanSetu profile, 
            you gain exclusive access to customized academic assets and strategic 
            career guidance. Let us provide the blueprint; you provide the ambition. </h3>
        """, unsafe_allow_html=True)


    if st.button("Sign Up/ Login"):
        auth_dialog()



# Dashboard 
else:
    st.markdown(
            "<h1 style='text-align:center;'>Dashboard</h1>",
            unsafe_allow_html=True
        )

    st.write("### Dashboard")
    st.write("Name:", st.session_state.name)
    st.write("Email:", st.session_state.email)
    st.write("Class:", st.session_state.user_class)
    st.write("Points:", st.session_state.points)

    st.divider()

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun() 
