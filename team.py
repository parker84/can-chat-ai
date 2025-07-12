import streamlit as st
from agno.agent import Agent
from agno.models.openai import OpenAIChat
# from agno.models.cohere import Cohere # TODO: fix this not working now
from textwrap import dedent
from agno.storage.sqlite import SqliteStorage
from agno.tools.reasoning import ReasoningTools
from agno.team.team import Team
from tools import fetch_url_contents, search_web
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
import os


DEBUG_MODE = os.getenv("DEBUG_MODE", "True").lower() == "true"

ADDITIONAL_CONTEXT = dedent("""
    Your outputs will be in markdown format so when using $ for money you need to escape it with a backslash.
    Focus on helping Canadian businesses, artists, creators, and the Canadian economy.
""")

# TODO: more search results with LLM reranking on top?
# TODO: switch over to cohere LLM

@st.cache_resource
def get_agent_team():
    product_finder_agent = Agent(
        name="Product Finder Agent",
        role="Find and recommend products",
        # model=Cohere(id="command-a-03-2025"),
        model=OpenAIChat(id="gpt-4.1-mini"),
        tools=[
            fetch_url_contents, 
            search_web, 
            ReasoningTools()
        ],
        instructions=[
            "Find and recommend the best Canadian products - that are from Canadian owned and operated businesses",
            "Don't forget to include classic / iconic and well known Canadian brands (when applicable) like: Roots, Lululemon, Canada Goose, Aritzia, Joe Fresh, Red Canoe, etc.",
            "Try to find 5-10 options ranked by ratings / your evaluation of the best options",
            "Include product information and links",
            "Always include sources (and link out to them)",
            "But don't just include the sources, pull out the relevant information from the sources",
            "Always include the product name, description, and link",
            "Always include the product price",
            "Always include the product rating",
            "Always include the product reviews",
            "Always include the product features",
            "Include a table at the bottom comparing all the products",
            "At a minimum include price, rating, features, link and Canadian owner / made as columns in the table",
            "Always include a section that explain for each brand / product whether it's canadian owned and or canadian made",
            "At the end consider asking the user if they products local to a certain region of Canada (ex: Toronto, Newfoundland, etc.)",
        ],
        additional_context=ADDITIONAL_CONTEXT,
        show_tool_calls=True,
        debug_mode=DEBUG_MODE,
        add_datetime_to_instructions=True,
        markdown=True,
    )

    service_finder_agent = Agent(
        name="Service Finder Agent",
        role="Find and recommend services",
        # model=Cohere(id="command-a-03-2025"),
        model=OpenAIChat(id="gpt-4.1-mini"),
        tools=[
            fetch_url_contents, 
            search_web, 
            ReasoningTools()
        ],
        instructions=[
            "Find and recommend the best Canadian services",
            "Consider the users location depending on the service (ex: electrician, plumber, etc.) -> ask for their general location",
            "Include service information and links",
            "Always include sources (and link out to them)",
            "But don't just include the sources, pull out the relevant information from the sources",
            "Always include the service name, description, and link",
            "Bias towards Canadian services that are Canadian owned and operated",
            "Include a table at the bottom comparing all the services",
            "At a minimum include price, rating, features, link and Canadian owner / made as columns in the table",
        ],
        additional_context=ADDITIONAL_CONTEXT,
        show_tool_calls=True,
        debug_mode=DEBUG_MODE,
        add_datetime_to_instructions=True,
        markdown=True,
    )

    brand_finder_agent = Agent(
        name="Brand Finder Agent",
        role="Find and recommend brands",
        # model=Cohere(id="command-a-03-2025"),
        model=OpenAIChat(id="gpt-4.1-mini"),
        tools=[
            fetch_url_contents, 
            search_web, 
            ReasoningTools()
    ],
        instructions=[
            "Find and recommend the best and most iconic Canadian brands",
            "Include brand information and links",
            "Always include sources (and link out to them)",
            "But don't just include the sources, pull out the relevant information from the sources",
            "Always include the brand name, description, and link",
            "Bias towards Canadian brands that are Canadian made",
            "Bias towards Canadian brands that are Canadian designed",
            "Bias towards Canadian brands that are Canadian owned and operated",
            "Include a table at the bottom comparing all the brands",
            "At a minimum include price, rating, features, link and Canadian owner / made as columns in the table",
        ],
        show_tool_calls=True,
        debug_mode=DEBUG_MODE,
        add_datetime_to_instructions=True,
        markdown=True,
        additional_context=ADDITIONAL_CONTEXT,
    )

    music_finder_agent = Agent(
        name="Music Finder Agent",
        role="Find and recommend music",
        # model=Cohere(id="command-a-03-2025"),
        model=OpenAIChat(id="gpt-4.1-mini"),
        tools=[
            fetch_url_contents, 
            search_web, 
            ReasoningTools()
        ],
        instructions=[
            "Find and recommend the best Canadian music",
            "Include music information and links",
            "Always include sources (and link out to them)",
            "But don't just include the sources, pull out the relevant information from the sources",
            "Always include the music name, description, and link",
            "Include a table at the bottom comparing all the music / artists",
            "At a minimum include the artist name, description, and link",
        ],
        show_tool_calls=True,
        debug_mode=DEBUG_MODE,
        add_datetime_to_instructions=True,
        markdown=True,
        additional_context=ADDITIONAL_CONTEXT,
    )

    movie_finder_agent = Agent(
        name="Movie Finder Agent",
        role="Find and recommend movies",
        # model=Cohere(id="command-a-03-2025"),
        model=OpenAIChat(id="gpt-4.1-mini"),
        tools=[
            fetch_url_contents, 
            search_web, 
            ReasoningTools()
        ],
        instructions=[
            "Find and recommend the best Canadian movies",
            "Include movie information and links",
            "Always include sources (and link out to them)",
            "But don't just include the sources, pull out the relevant information from the sources",
            "Always include the movie name, description, and link",
            "Include imdb / rotten tomatoes / google ratings",
            "Summarize the results in a table at the bottom",
            "Callout for each show what makes it canadian",
        ],
        show_tool_calls=True,
        debug_mode=DEBUG_MODE,
        add_datetime_to_instructions=True,
        markdown=True,
        additional_context=ADDITIONAL_CONTEXT,
    )

    tv_show_finder_agent = Agent(
        name="TV Show Finder Agent",
        role="Find and recommend TV shows",
        # model=Cohere(id="command-a-03-2025"),
        model=OpenAIChat(id="gpt-4.1-mini"),
        tools=[
            fetch_url_contents,   
            search_web, 
            ReasoningTools()
        ],
        instructions=[
            "Find and recommend the best Canadian TV shows",
            "Include TV show information and links",
            "Always include sources (and link out to them)",
            "But don't just include the sources, pull out the relevant information from the sources",
            "Always include the TV show name, description, and link",
            "Include imdb / rotten tomatoes / google ratings",
            "Summarize the results in a table at the bottom",
            "Callout for each show what makes it canadian",
        ],
        show_tool_calls=True,
        debug_mode=DEBUG_MODE,
        add_datetime_to_instructions=True,
        markdown=True,
        additional_context=ADDITIONAL_CONTEXT,
    )

    book_finder_agent = Agent(
        name="Book Finder Agent",
        role="Find and recommend books",
        # model=Cohere(id="command-a-03-2025"),
        model=OpenAIChat(id="gpt-4.1-mini"),
        tools=[
            fetch_url_contents, 
            search_web, 
            ReasoningTools()
        ],
        instructions=[
            "Find and recommend the best Canadian books",
            "Include book information and links",
            "Always include sources (and link out to them)",
            "But don't just include the sources, pull out the relevant information from the sources",
            "Always include the book name, description, and link",
            "Include ratings / accolades / reviews / awards",
            "Summarize the results in a table at the bottom",
            "Callout for each book what makes it canadian (ex: author is canadian, book is about canada, etc.)",
        ],
        show_tool_calls=True,
        debug_mode=DEBUG_MODE,
        add_datetime_to_instructions=True,
        markdown=True,
        additional_context=ADDITIONAL_CONTEXT,
    )

    artist_finder_agent = Agent(
        name="Artist Finder Agent",
        role="Find and recommend artists",
        # model=Cohere(id="command-a-03-2025"),
        model=OpenAIChat(id="gpt-4.1-mini"),
        tools=[
            fetch_url_contents, 
            search_web, 
            ReasoningTools()
        ],
        instructions=[
            "Find and recommend the best Canadian artists",
            "Include artist information and links",
            "Always include sources (and link out to them)",
            "But don't just include the sources, pull out the relevant information from the sources",
            "Always include the artist name, description, and link",
        ],
        show_tool_calls=True,
        debug_mode=DEBUG_MODE,
        add_datetime_to_instructions=True,
        markdown=True,
        additional_context=ADDITIONAL_CONTEXT,
    )

    gift_finder_agent = Agent(
        name="Gift Finder Agent",
        role="Find and recommend gifts",
        # model=Cohere(id="command-a-03-2025"),
        model=OpenAIChat(id="gpt-4.1-mini"),
        respond_directly=False,
        tools=[
            fetch_url_contents, 
            search_web, 
            ReasoningTools()
        ],
        instructions=[
            "Find and recommend the best Canadian gifts",
            "Try to make the gift very personalized by asking the user questions about the person you're recommending a gift for",
            "Do not recommend gifts without a link that actually works, and include the correct ratings and the volume of reviews",
            "Then use that information to recommend the best gift for them",
            "Include gift information and links",
            "Always include sources (and link out to them)",
            "But don't just include the sources, pull out the relevant information from the sources",
            "Always include the gift name, description, and link",
            "Always include the gift price",
            "Always include the gift rating",
            "Always include the gift reviews",
            "Always include the gift features",
            "Bias towards Canadian gifts that are Canadian made",
            "Bias towards Canadian gifts that are Canadian designed",
            "Bias towards Canadian gifts that are Canadian owned and operated",
        ],
        show_tool_calls=True,
        debug_mode=DEBUG_MODE,
        add_datetime_to_instructions=True,
        additional_context=ADDITIONAL_CONTEXT,
    )

    car_finder_agent = Agent(
        name="Car Finder Agent",
        role="Find and recommend cars",
        model=OpenAIChat(id="gpt-4.1-mini"),
        tools=[
            fetch_url_contents, 
            search_web, 
            ReasoningTools()
        ],
        instructions=[
            "Find and recommend the best cars that are made in Canada",
            "Include car information and links",
            "Try to find 5-10 options ranked by ratings / your evaluation of the best options",
            "Always include sources (and link out to them)",
            "But don't just include the sources, pull out the relevant information from the sources",
            "Always include the car name, description, and link",
            "Always include the car price",
            "Always include the car rating",
            "Always include the car reviews",
            "Always include the car features",
            "Summarize the results in a table at the bottom",
            "For each car include a section that explains where in canada it's made and to what extent it's made in canada",
        ],
        additional_context=ADDITIONAL_CONTEXT,
        show_tool_calls=True,
        debug_mode=DEBUG_MODE,
        add_datetime_to_instructions=True,
        markdown=True,
    )

    # Database file for memory and storage
    db_file = "tmp/agent.db"

    # Initialize memory.v2
    memory = Memory(
        # Use any model for creating memories
        # model=Cohere(id="command-a-03-2025"),
        model=OpenAIChat(id="gpt-4.1-mini"),
        db=SqliteMemoryDb(table_name="user_memories", db_file=db_file),
    )

    agent_team = Team(
        name="Canadian AI",
        # description="A team of AI agents that can help you accomplish a number of things that are biased towards supporting Canadian businesses, artists, creators, and the Canadian economy.",
        description="You're a Canadian AI assistant that can help users accomplish a multitude of tasks (ex: find a gift, find a product, find a service, find a movie, find a book, find a tv show, find a music artist, find a brand, etc.) but you are intentionally biased towards supporting Canadian businesses, artists, creators, and the Canadian economy.",
        mode="route",
        # mode="collaborate",
        members=[
            product_finder_agent,
            service_finder_agent,
            brand_finder_agent,
            music_finder_agent,
            movie_finder_agent,
            tv_show_finder_agent,
            book_finder_agent,
            artist_finder_agent,
            gift_finder_agent,
            car_finder_agent
        ],
        tools=[
            fetch_url_contents, 
            search_web, 
            ReasoningTools(),
        ],
        # model=Cohere(id="command-a-03-2025"),
        model=OpenAIChat(id="gpt-4.1-mini"), # this does better w yoga pants question
        instructions=dedent(
            """
            Answer the user's question to the best of your abilities.
            But generally bias towards supporting Canadian businesses, artists, creators, and the Canadian economy.

            Leverage the team of agents you have to accomplish the user's request.
            - if the user is asking for / about a product, use the product finder agent.
            - if the user is asking for / about a service, use the service finder agent.
            - if the user is asking for / about a brand, use the brand finder agent.
            - if the user is asking for / about music, use the music finder agent.
            - if the user is asking for / about a movie, use the movie finder agent.
            - if the user is asking for / about a tv show, use the tv show finder agent.
            - if the user is asking for / about a book, use the book finder agent.
            - if the user is asking for / about an artist, use the artist finder agent.
            - if the user is asking for / about a gift, use the gift finder agent.
            - if the user is asking for / about a car, use the car finder agent.

            Ask questions to get a better understanding of the user's needs, but  not too many to annoy the user.
            Usually keep it to 1 follow up question max before trying to answer the user's question.
            """
        ),
        show_tool_calls=True,
        debug_mode=DEBUG_MODE,
        add_datetime_to_instructions=True,
        show_members_responses=True,
        markdown=True,
        additional_context=ADDITIONAL_CONTEXT,
        # ----------memory----------
        # adding previous 5 questions and answers to the prompt
        # read more here: https://docs.agno.com/memory/introduction
        storage=SqliteStorage(table_name="agent_sessions", db_file=db_file),
        enable_team_history=True,
        num_history_runs=5,
        # adding agentic memory: "With Agentic Memory, The Agent itself creates, updates and deletes memories from user conversations."
        # read more here: https://docs.agno.com/memory/memory
        enable_agentic_memory=True,
        memory=memory,
    )
    return agent_team


# help me find a gift for my father
# he's 62, retired, loves travelling, into star wars, hockey (especially the leafs), and he's a bit of a nerd (likes star wars, star trek, space, etc.)


# I want to find some new music
# I like Rock recently have been into alanis morset, and love the tragically hip