import streamlit as st

# Dummy Data --- Replace it by DB/ JSON
CHAPTERS = {
    "Algebra": ["Linear Equations", "Quadratic Equations"],
    "Geometry": ["Triangles", "Circles"],
    "Science": ["Motion", "Force"]
}

def dashboard():

    with st.sidebar:

        st.title("📚 GyaanSetu 📚")

        st.markdown("---")
        st.write("**User Info**")
        st.write("Name:", st.session_state.name)
        st.write("Class:", st.session_state.user_class)
        st.write("Points:", st.session_state.points)

        st.markdown("---")

        st.subheader("Select Chapter")
        selected_chapter = st.radio(
            "Chapters",
            list(CHAPTERS.keys())
        )

        st.subheader("Select Module")
        selected_module = st.radio(
            "Modules",
            CHAPTERS[selected_chapter]
        )

        st.markdown("---")

        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()


    # main page area
    st.markdown(
        "<h1 style='text-align:center;'>Dashboard</h1>",
        unsafe_allow_html=True
    )

    st.write(f"### Welcome, {st.session_state.name}")
    st.write("Class:", st.session_state.user_class)
    st.write("Points:", st.session_state.points)

    st.divider()

    st.subheader("Selected Path")
    st.write(f"**Chapter:** {selected_chapter}")
    st.write(f"**Module:** {selected_module}")

    st.divider()

    if st.button("Start Quiz", use_container_width=True):
        st.success(f"Starting Quiz for {selected_module}")
        # quiz function call