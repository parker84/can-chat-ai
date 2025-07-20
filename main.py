import streamlit as st
from typing import Iterator
from agno.run.response import RunResponse
from team import get_agent_team
from random import choice

def add_floating_button():
    # Use st.markdown with a direct HTML anchor tag for the button instead of JS, for better compatibility.
    st.markdown(
        """
    <style>
        .coffee-btn {
            position: fixed;
            bottom: 40px;
            right: 40px;
            z-index: 100;
            background: #f8f9fa;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.10);
            padding: 0;
            opacity: 0.85;
            transition: opacity 0.2s;
        }
        .coffee-btn:hover {
            opacity: 1;
        }
        .coffee-btn a {
            display: block;
            padding: 10px 20px;
            color: #666;
            text-decoration: none;
            font-weight: normal;
            font-size: 15px;
            background: none;
            border-radius: 8px;
            transition: background 0.2s, color 0.2s;
        }
        .coffee-btn a:hover {
            background: #f1f3f4;
            color: #222;
        }
    </style>
    <div class="coffee-btn">
        <a href="https://buymeacoffee.com/brydon" target="_blank" rel="noopener noreferrer">Buy me a coffee ☕️</a>
    </div>
    """,
        unsafe_allow_html=True,
    )

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
st.caption("AI that is biased to support Canadian businesses and the Canadian economy 🍁")

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

add_floating_button()

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