
import streamlit as st


def handle_auth_callback():
    # Streamlit handles Google's OAuth callback automatically.
    pass


def get_current_user():
    if not getattr(st.user, "is_logged_in", False):
        return None

    return {
        "id": st.user.sub,
        "email": getattr(st.user, "email", ""),
        "name": getattr(st.user, "name", ""),
    }


def sign_in_with_google():
    st.button(
        "Continue with Google",
        on_click=st.login,
        args=["google"],
        use_container_width=True,
    )
