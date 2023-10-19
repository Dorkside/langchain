import streamlit as st

from dotenv import load_dotenv
load_dotenv()

from langchain.globals import set_llm_cache, get_llm_cache
from langchain.cache import InMemoryCache
set_llm_cache(InMemoryCache())

from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI()

from langchain.prompts.chat import ChatPromptTemplate

template = "You are a helpful assistant that translates {input_language} to {output_language}."
human_template = "{text}"

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", human_template),
])

chain = chat_prompt | ChatOpenAI()

st.write("## Chatbot")
st.write("This is a chatbot that translates from English to French.")

text = st.text_input("Enter your message here:")

res = chain.invoke({"input_language": "English", "output_language": "French", "text": text})

st.write("### Response:")
st.write(res)