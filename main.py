import streamlit as st
from typing import Iterator
from agno.run.response import RunResponse
from team import get_agent_team
from random import choice

# Set page config
st.set_page_config(
    page_title="Canadian AI",
    page_icon="🍁",
    initial_sidebar_state="collapsed",
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

def parse_stream(stream: Iterator[RunResponse]):
    for chunk in stream:
        if hasattr(chunk, "event") and chunk.event == 'TeamRunResponseContent':
            yield chunk.content

# TODO: add sidebar with chat history

# App title and description
st.title("Canadian AI")
st.caption("Built on Canadian LLMs and is biased to support Canadian businesses, creators, and the Canadian economy 🍁")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🍁" if message["role"] == "assistant" else "💁‍♀️"):
        st.markdown(message["content"])

@st.cache_data
def get_placeholder():
    return choice([
        "Help me find a gift for my father",
        "I want to find some new music",
        "I'm in the market for a pair of jeans",
        "I want to find a new movie to watch",
        "What book should I read next?",
        "What's the top tv show to watch right now?",
        "I need a new car",
        "I'm trying to find some new yoga pants",
        "I'm looking for a new pair of shoes",
    ])

if prompt := st.chat_input(
        placeholder=get_placeholder()
    ):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user", avatar="💁‍♀️"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant", avatar="🍁"):
        message_placeholder = st.empty()
        
        with st.spinner("Thinking..."):
            agent_team = get_agent_team()
            
            stream: Iterator[RunResponse] = agent_team.run(
                prompt, 
                stream=True, 
                auto_invoke_tools=True,
                user_id="ava",
            )
            full_response = st.write_stream(parse_stream(stream))

        st.session_state.messages.append({"role": "assistant", "content": full_response})