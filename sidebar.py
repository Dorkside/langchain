import streamlit as st
from choices import CHOICES

from database import get_db_connection


class Sidebar:
    def __init__(self):
        with st.sidebar:
            st.subheader("Options")
            st.session_state["temperature"] = st.slider(
                "Temperature", 0.0, 2.0, st.session_state["temperature"]
            )

            st.session_state["template"] = st.selectbox("System", CHOICES.keys())

            st.subheader("History")

            conversations = self.get_conversations()

            # for each conversation in the database, add a link to the sidebar
            for conversation in conversations:
                st.link_button(
                    conversation["title"],
                    type="secondary",
                    use_container_width=True,
                    url=f"?conversation={conversation['id']}",
                )

    def get_conversations(self):
        conn = get_db_connection()
        conversations = conn.execute("SELECT * FROM conversations").fetchall()
        conn.close()
        return conversations
