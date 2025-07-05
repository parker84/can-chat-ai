import streamlit as st
from typing import Iterator
from agno.run.response import RunResponse
from team import get_agent_team

# Set page config
st.set_page_config(
    page_title="Canadian AI",
    page_icon="🍁",
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

def parse_stream(stream):
    for chunk in stream:
        if chunk.content is not None:
            yield chunk.content

# TODO: add sidebar with chat history

# App title and description
st.title("Canadian AI")
st.caption("Built on Canadian LLMs and is biased to support Canadian businesses, creators, and the Canadian economy 🍁")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🍁" if message["role"] == "assistant" else "💁‍♀️"):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input(
        placeholder="How can I help you today?"
    ):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user", avatar="💁‍♀️"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant", avatar="🍁"):
        message_placeholder = st.empty()
        full_response = ""
        
        with st.spinner("Thinking..."):
            agent_team = get_agent_team()
            
            stream: Iterator[RunResponse] = agent_team.run(
                prompt, 
                stream=True, 
                auto_invoke_tools=True,
                user_id="ava",
            )
            response = st.write_stream(parse_stream(stream))

        st.session_state.messages.append({"role": "assistant", "content": full_response}) 