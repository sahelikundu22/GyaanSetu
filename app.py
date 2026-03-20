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

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ---------- LOGIN PAGE ----------
if not st.session_state.logged_in:

    # Background style
    st.markdown("""
    <style>
    .main {
        background: linear-gradient(to right, #0f172a, #1e293b);
    }

    .title {
        text-align:center;
        font-size:60px;
        font-weight:700;
        color:#ffffff;
    }

    .subtitle {
        text-align:center;
        font-size:20px;
        color:#cbd5e1;
    }

    </style>
    """, unsafe_allow_html=True)
    st.markdown("<div class='title'>📚 GyaanSetu</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Connecting Ambition with Education</div>", unsafe_allow_html=True)

    st.divider()

    col1, col2, col3 = st.columns([2,3,2])

    with col2:
        st.markdown("<div class='box'>", unsafe_allow_html=True)

        st.markdown("### 🚀 Get Started")

        st.write("Create your profile to unlock personalized learning and AI-powered tools.")

        if st.button("🔐 Sign Up / Login", use_container_width=True):
            auth_dialog()

        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    st.markdown("""
        <div style='text-align:center; font-size:18px; color:#555;'>
        Generic resources only take you so far. By creating your GyaanSetu profile, 
        you gain access to customized academic assets and smart learning tools.
        </div>
    """, unsafe_allow_html=True)


# ---------- DASHBOARD ----------
else:
    dashboard()