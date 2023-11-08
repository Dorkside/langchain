import os
import streamlit as st


def set_env_vars():
    if "langchain_api_key" in st.secrets:
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
        os.environ["LANGCHAIN_API_KEY"] = st.secrets.langchain_api_key
        os.environ["LANGCHAIN_PROJECT"] = "local-chat"

    if "openai_api_key" in st.secrets:
        os.environ["OPENAI_API_KEY"] = st.secrets.openai_api_key
