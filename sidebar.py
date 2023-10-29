import streamlit as st

class Sidebar:
    def __init__(self):
        with st.sidebar:
            st.subheader("Options")
            st.session_state['temperature'] = st.slider("Temperature", 0.0, 2.0, st.session_state['temperature'])

            st.subheader("History")
            st.link_button('Conversation #1', type="secondary", use_container_width=True, url="?conversation=1")