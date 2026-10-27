
import streamlit as st


def render_home_page():
    st.subheader("Welcome to your study workspace 👋")
    st.write(
        "Learn, explore your study materials, and prepare smarter with AI."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("### 💬 Ask AI")
            st.write(
                "Get answers to your questions based on your uploaded PDFs."
            )

            if st.button("Open Ask AI", use_container_width=True):
                st.session_state.page = "Ask AI"
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown("### 📝 Summarize")
            st.write(
                "Create quick summaries, detailed notes, and key points "
                "from your study materials."
            )

            if st.button("Open Summarize", use_container_width=True):
                st.session_state.page = "Summarize"
                st.rerun()

    col3, col4 = st.columns(2)

    with col3:
        with st.container(border=True):
            st.markdown("### 🎯 Practice Quiz")
            st.write(
                "Test your understanding with multiple-choice questions "
                "and explanations."
            )

            if st.button("Open Practice Quiz", use_container_width=True):
                st.session_state.page = "Practice Quiz"
                st.rerun()

    with col4:
        with st.container(border=True):
            st.markdown("### 📚 My Documents")
            st.write("Upload and manage your study PDFs.")

            if st.button("View Documents", use_container_width=True):
                st.session_state.page = "My Documents"
                st.rerun()
