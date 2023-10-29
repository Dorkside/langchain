from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.prompts import PromptTemplate
import streamlit as st

st.set_page_config(page_title="StreamlitChatMessageHistory", page_icon="📖")
st.title("📖 StreamlitChatMessageHistory")

"""
# Career agent
This is a career agent that helps you plan your career.
"""


# Set up memory
msgs = StreamlitChatMessageHistory(key="langchain_messages")
memory = ConversationBufferMemory(chat_memory=msgs)
if len(msgs.messages) == 0:
    msgs.add_ai_message("Please tell me about yourself.")

view_messages = st.expander("View the message contents in session state")

# Get an OpenAI API Key before continuing
if "openai_api_key" in st.secrets:
    openai_api_key = st.secrets.openai_api_key
else:
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Enter an OpenAI API Key to continue")
    st.stop()

class StreamHandler(StreamingStdOutCallbackHandler):
    def __init__(self, container, initial_text="", display_method='markdown'):
        self.container = container
        self.text = initial_text
        self.display_method = display_method

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        display_function = getattr(self.container, self.display_method, None)
        if display_function is not None:
            display_function(self.text)
        else:
            raise ValueError(f"Invalid display_method: {self.display_method}")

# Render current messages from StreamlitChatMessageHistory
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

# Set up the LLMChain, passing in memory
template = """
You are a helpful career planner that tries to help people plan their career.

Your first task is to determine what the person wants to do with their life.
For this you should ask them specific targetted questions to provide at least 3 options for them to look into.
Keep asking follow up questions until you are very confident that you have a good idea of what they want to do.

{history}
Human: {human_input}
AI: """

# If user inputs a new prompt, generate and draw a new response
if user_input := st.chat_input():
    st.chat_message("human").write(user_input)
    chat_box = st.chat_message("ai").empty()
    stream_handler = StreamHandler(chat_box, display_method='write')

    prompt = PromptTemplate(input_variables=["history", "human_input"], template=template)
    chat = ChatOpenAI(openai_api_key=openai_api_key, streaming=True, callbacks=[stream_handler], temperature=0, model_name="gpt-4")
    llm_chain = LLMChain(llm=chat, prompt=prompt, memory=memory)

    # Note: new messages are saved to history automatically by Langchain during run
    response = llm_chain.run(user_input)

# Draw the messages at the end, so newly generated ones show up immediately
with view_messages:
    """
    Memory initialized with:
    ```python
    msgs = StreamlitChatMessageHistory(key="langchain_messages")
    memory = ConversationBufferMemory(chat_memory=msgs)
    ```

    Contents of `st.session_state.langchain_messages`:
    """
    view_messages.json(st.session_state.langchain_messages)
