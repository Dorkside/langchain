import streamlit as st
from choices import CHOICES

class Sidebar:
    def __init__(self):
        print(CHOICES)
        with st.sidebar:
            st.subheader("Options")
            st.session_state['temperature'] = st.slider(
                "Temperature", 0.0, 2.0, st.session_state['temperature'])

            st.session_state['template'] = st.selectbox(
                "System",
                CHOICES.keys()
            )

            st.subheader("History")
            st.link_button('Conversation #1', type="secondary",
                           use_container_width=True, url="?conversation=1")
