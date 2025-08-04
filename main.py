import streamlit as st
from typing import Iterator
from agno.run.response import RunResponse
from team import get_agent_team
from random import choice
import uuid

# TODO: investigate why I could login with parkerbrydon@gmail.com?
# TODO: look into the puremd api key -> do I need to setup a paid account?

def login_screen():
    st.header("Welcome to Canadian AI 🍁")
    st.markdown("#### Please log in to continue 👇")
    st.button("🔐 Log in with Google", on_click=st.login, type="primary")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())  # Generate new UUID

def add_floating_button(
    link: str = "https://buymeacoffee.com/brydon",
    emoji: str = "☕️",
    text: str = "Buy me a coffee",
    position: dict = {"bottom": "40px", "right": "40px"},
    colors: dict = {
        "background": "#f8f9fa",
        "text": "#666",
        "text_hover": "#222",
        "background_hover": "#f1f3f4"
    }
):
    """Add a floating button to the page with customizable properties."""
    # Initialize session state for page refresh counter
    if "page_refresh_count" not in st.session_state:
        st.session_state.page_refresh_count = 0
    
    # Increment the counter on each page load
    st.session_state.page_refresh_count += 1
    
    # Use st.markdown with a direct HTML anchor tag for the button
    st.markdown(
        f"""
    <style>
        .coffee-btn {{
            position: fixed;
            bottom: {position["bottom"]};
            right: {position["right"]};
            z-index: 100;
            background: {colors["background"]};
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.10);
            padding: 0;
            opacity: 0.85;
            transition: opacity 0.2s;
            min-width: 0;
        }}
        .coffee-btn:hover {{
            opacity: 1;
        }}
        .coffee-btn a {{
            display: block;
            padding: 10px 20px 10px 20px;
            color: {colors["text"]};
            text-decoration: none;
            font-weight: normal;
            font-size: 15px;
            background: none;
            border-radius: 8px;
            transition: background 0.2s, color 0.2s;
        }}
        .coffee-btn a:hover {{
            background: {colors["background_hover"]};
            color: {colors["text_hover"]};
        }}
    </style>
    <div class="coffee-btn" id="coffee-btn">
        <a href="{link}" target="_blank" rel="noopener noreferrer">
            {emoji if st.session_state.page_refresh_count > 1 else f"{text} {emoji}"}
        </a>
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

# Handle authentication
if not st.user.is_logged_in:
    login_screen()
    
    # Show waitlist signup form
    st.markdown("---")
    st.write("Not yet approved for access? Join our waitlist!")
    st.write("[Join the waitlist 📬](https://stan.store/brydon/p/canadian-ai-waitlist-)")
else:
    # Show the main app interface
    st.sidebar.button("Log out", on_click=st.logout, type="secondary")
    st.title("Canadian AI")
    st.caption("AI that is biased to support Canadian businesses and the Canadian economy 🍁")
    st.write(f"Welcome, {st.user.name}! 👋") 
    st.write("How can I help you today?")

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

# add_floating_button(
#     link="https://buymeacoffee.com/brydon",
#     emoji="☕️",
#     text="Buy me a coffee",
#     position={"bottom": "40px", "right": "40px"},
#     colors={"background": "#f8f9fa", "text": "#666", "text_hover": "#222", "background_hover": "#f1f3f4"}
# )

add_floating_button(
    link="https://forms.gle/LNdMMnniVND7qTRq8",
    emoji="❤️",
    text="Help us improve",
    position={"bottom": "40px", "right": "40px"},
    colors={"background": "#f8f9fa", "text": "#666", "text_hover": "#222", "background_hover": "#f1f3f4"}
)

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
                user_id=st.user.email, # stores memories for the user
                session_id=st.session_state.session_id, # stores the session history for each user
            )
            full_response = st.write_stream(parse_stream(stream))

        st.session_state.messages.append({"role": "assistant", "content": full_response})