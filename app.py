import streamlit as st
from database import init_db
from auth import auth_dialog
from dashboard import dashboard

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

    col1, col2, col3 = st.columns([3, 1, 3])
    with col2:
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


    col1, col2, col3 = st.columns([3, 1, 3])

    with col2:
        if st.button("Sign Up / Login", use_container_width=True):
            auth_dialog()


# Dashboard 
else:
    dashboard()
