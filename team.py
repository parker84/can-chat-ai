import streamlit as st
from agno.agent import Agent
from agno.models.openai import OpenAIChat
# from agno.models.cohere import Cohere # TODO: fix this not working now
from textwrap import dedent
from agno.storage.sqlite import SqliteStorage
# from agno.knowledge.csv import CSVKnowledgeBase
from agno.tools.reasoning import ReasoningTools
# from agno.vectordb.chroma import ChromaDb
from agno.team.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from tools import fetch_url_contents, search_web
# from agno.tools.yfinance import YFinanceTools
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
import os

# TODO: deal w the massive outputs sometimes - is it not properly leveraging the sources?
# TODO: is it properly understanding things or just regurgitating the sources?

DEBUG_MODE = os.getenv("DEBUG_MODE", "True").lower() == "true"

# canadian_shopify_businesses_knowledge_base = CSVKnowledgeBase(
#     path="data/shop_canada_data.csv", # from here: https://github.com/parker84/shop-canada
#     vector_db=ChromaDb(collection="canadian_shopify_businesses"),
#     num_documents=10,  # Number of documents to return on search
#     # chunking_strategy=AgenticChunking(), # agentic chunking: https://docs.agno.com/chunking/agentic-chunking
# )

# TODO: make a team of agents
# TODO: give each agent reasoning + search capabilities 
# TODO: fix the search capabilities
# TODO: more search results with LLM reranking on top?
# TODO: switch over to cohere LLM
# TODO: let's make it route instead of collaborate

# TODO: bring in the team of agents
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
            # ReasoningTools()
        ],
        instructions=[
            "Find and recommend the best Canadian products",
            "Include product information and links",
            "Always include sources (and link out to them)",
            "But don't just include the sources, pull out the relevant information from the sources",
            "Always include the product name, description, and link",
            "Always include the product price",
            "Always include the product rating",
            "Always include the product reviews",
            # "Always include the product images",
            "Always include the product features",
            "Bias towards Canadian products from Canadian owned and operated businesses",
            "Bias towards Canadian products that are made in Canada",
            "At the end consider asking the user if they products local to a certain region of Canada (ex: Toronto, Newfoundland, etc.)",
        ],
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
            # ReasoningTools()
        ],
        instructions=[
            "Find and recommend the best Canadian services",
            "Consider the users location depending on the service (ex: electrician, plumber, etc.) -> ask for their general location",
            "Include service information and links",
            "Always include sources (and link out to them)",
            "But don't just include the sources, pull out the relevant information from the sources",
            "Always include the service name, description, and link",
            "Bias towards Canadian services that are Canadian owned and operated",
        ],
        show_tool_calls=True,
        debug_mode=DEBUG_MODE,
        add_datetime_to_instructions=True,
        markdown=True,
    )

    # brand_finder_agent = Agent(
    #     name="Brand Finder Agent",
    #     role="Find and recommend brands",
    #     # model=Cohere(id="command-a-03-2025"),
    #     model=OpenAIChat(id="gpt-4.1-mini"),
    #     tools=[
    #         fetch_url_contents, 
    #         search_web, 
    #         # ReasoningTools()
    #         # DuckDuckGoTools()
#     ],
    #     instructions=[
    #         "Find and recommend the best and most iconic Canadian brands",
    #         "Include brand information and links",
    #         "Always include sources (and link out to them)",
    #         "But don't just include the sources, pull out the relevant information from the sources",
    #         "Always include the brand name, description, and link",
    #         "Bias towards Canadian brands that are Canadian made",
    #         "Bias towards Canadian brands that are Canadian designed",
    #         "Bias towards Canadian brands that are Canadian owned and operated",
    #     ],
    #     show_tool_calls=True,
    #     debug_mode=DEBUG_MODE,
    #     add_datetime_to_instructions=True,
    #     markdown=True,
    # )

    # music_finder_agent = Agent(
    #     name="Music Finder Agent",
    #     role="Find and recommend music",
    #     # model=Cohere(id="command-a-03-2025"),
    #     model=OpenAIChat(id="gpt-4.1-mini"),
    #     tools=[
    #         fetch_url_contents, 
    #         search_web, 
    #         # ReasoningTools()
    #         # DuckDuckGoTools()
    #     ],
    #     instructions=[
    #         "Find and recommend the best Canadian music",
    #         "Include music information and links",
    #         "Always include sources (and link out to them)",
    #         "But don't just include the sources, pull out the relevant information from the sources",
    #         "Always include the music name, description, and link",
    #     ],
    #     show_tool_calls=True,
    #     debug_mode=DEBUG_MODE,
    #     add_datetime_to_instructions=True,
    #     markdown=True,
    # )

    # movie_finder_agent = Agent(
    #     name="Movie Finder Agent",
    #     role="Find and recommend movies",
    #     # model=Cohere(id="command-a-03-2025"),
    #     model=OpenAIChat(id="gpt-4.1-mini"),
    #     tools=[
    #         # fetch_url_contents, 
    #         # search_web, 
    #         # ReasoningTools()
    #         DuckDuckGoTools()
    #     ],
    #     instructions=[
    #         "Find and recommend the best Canadian movies",
    #         "Include movie information and links",
    #         "Always include sources (and link out to them)",
    #         "But don't just include the sources, pull out the relevant information from the sources",
    #         "Always include the movie name, description, and link",
    #     ],
    #     show_tool_calls=True,
    #     debug_mode=DEBUG_MODE,
    #     add_datetime_to_instructions=True,
    #     markdown=True,
    # )

    # tv_show_finder_agent = Agent(
    #     name="TV Show Finder Agent",
    #     role="Find and recommend TV shows",
    #     # model=Cohere(id="command-a-03-2025"),
    #     model=OpenAIChat(id="gpt-4.1-mini"),
    #     tools=[
    #         fetch_url_contents,   
    #         search_web, 
    #         # ReasoningTools()
    #         # DuckDuckGoTools()
    #     ],
    #     instructions=[
    #         "Find and recommend the best Canadian TV shows",
    #         "Include TV show information and links",
    #         "Always include sources (and link out to them)",
    #         "But don't just include the sources, pull out the relevant information from the sources",
    #         "Always include the TV show name, description, and link",
    #     ],
    #     show_tool_calls=True,
    #     debug_mode=DEBUG_MODE,
    #     add_datetime_to_instructions=True,
    #     markdown=True,
    # )

    # book_finder_agent = Agent(
    #     name="Book Finder Agent",
    #     role="Find and recommend books",
    #     # model=Cohere(id="command-a-03-2025"),
    #     model=OpenAIChat(id="gpt-4.1-mini"),
    #     tools=[
    #         fetch_url_contents, 
    #         search_web, 
    #         # ReasoningTools()
    #         # DuckDuckGoTools()
    #     ],
    #     instructions=[
    #         "Find and recommend the best Canadian books",
    #         "Include book information and links",
    #         "Always include sources (and link out to them)",
    #         "But don't just include the sources, pull out the relevant information from the sources",
    #         "Always include the book name, description, and link",
    #     ],
    #     show_tool_calls=True,
    #     debug_mode=DEBUG_MODE,
    #     add_datetime_to_instructions=True,
    #     markdown=True,
    # )

    # artist_finder_agent = Agent(
    #     name="Artist Finder Agent",
    #     role="Find and recommend artists",
    #     # model=Cohere(id="command-a-03-2025"),
    #     model=OpenAIChat(id="gpt-4.1-mini"),
    #     tools=[
    #         fetch_url_contents, 
    #         search_web, 
    #         # ReasoningTools()
    #         # DuckDuckGoTools()
    #     ],
    #     instructions=[
    #         "Find and recommend the best Canadian artists",
    #         "Include artist information and links",
    #         "Always include sources (and link out to them)",
    #         "But don't just include the sources, pull out the relevant information from the sources",
    #         "Always include the artist name, description, and link",
    #     ],
    #     show_tool_calls=True,
    #     debug_mode=DEBUG_MODE,
    #     add_datetime_to_instructions=True,
    #     markdown=True,
        
    # )

    # gift_finder_agent = Agent(
    #     name="Gift Finder Agent",
    #     role="Find and recommend gifts",
    #     # model=Cohere(id="command-a-03-2025"),
    #     model=OpenAIChat(id="gpt-4.1-mini"),
    #     respond_directly=False,
    #     tools=[
    #         # fetch_url_contents, 
    #         # search_web, 
    #         # ReasoningTools()
    #         # DuckDuckGoTools()
    #     ],
    #     instructions=[
    #         "Find and recommend the best Canadian gifts",
    #         "Try to make the gift very personalized by asking the user questions about the person you're recommending a gift for",
    #         "Do not recommend gifts without a link that actually works, and include the correct ratings and the volume of reviews",
    #         "Then use that information to recommend the best gift for them",
    #         "Include gift information and links",
    #         "Always include sources (and link out to them)",
    #         "But don't just include the sources, pull out the relevant information from the sources",
    #         "Always include the gift name, description, and link",
    #         "Always include the gift price",
    #         "Always include the gift rating",
    #         "Always include the gift reviews",
    #         # "Always include the gift images",
    #         "Always include the gift features",
    #         "Bias towards Canadian gifts that are Canadian made",
    #         "Bias towards Canadian gifts that are Canadian designed",
    #         "Bias towards Canadian gifts that are Canadian owned and operated",
    #     ],
    #     # show_tool_calls=True,
    #     # debug_mode=DEBUG_MODE,
    #     add_datetime_to_instructions=True,
    # )

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
            # brand_finder_agent,
            # music_finder_agent,
            # movie_finder_agent,
            # tv_show_finder_agent,
            # book_finder_agent,
            # artist_finder_agent,
            # gift_finder_agent,
        ],
        tools=[
            fetch_url_contents, 
            search_web, 
            ReasoningTools(),
            # DuckDuckGoTools()
        ],
        # model=Cohere(id="command-a-03-2025"),
        model=OpenAIChat(id="gpt-4.1-mini"), # this does better w yoga pants question
        #            DO NOT respond directly to the user, let an agent respond to the user.


            # TODO: make a car finder agent and put this context below into it
            # If there aren't any Canadian businesses that meet the user's request, 
            # then look for businesses that are still making the product or service in Canada.

            # Examples:
            # - there aren't Canadian car companies, but some cars are made in Canada.

            # If you're not 100% certain about whether something is made in Canada vs what isn't then use the search tools to find out.
            # When searching though -> just don't search for products available in Canada.
            # Search for products that are made in Canada.

            # Note: not everything you need to recommend has to be made in Canada.
            # But they should at least be from Canadian owned and operated businesses if not.

            # Examples:
            # - Roots is a Canadian brand, but not everything they sell is made in Canada -> but you still recommend this iconic Canadian brand.
            # - Lululemon is a Canadian brand, but not everything they sell is made in Canada -> but you still recommend this iconic Canadian brand.

        # TODO: fix the lululemon response around yoga pants
        # TODO: 

        instructions=dedent(
            # """
            # Answer the user's question to the best of your abilities.
            # But generally bias towards supporting Canadian businesses, artists, creators, and the Canadian economy.
            # Leverage the team of agents you have to accomplish the user's request.
            # """
            """
            Answer the user's question to the best of your abilities.
            
            But generally bias towards supporting Canadian businesses, artists, creators, and the Canadian economy.
            
            Examples: 
            - when providing product / service recommendations bias towards canadian owned and operated businesses.
            - when providing music recommendations bias towards canadian artists.
            - when providing movie recommendations bias towards canadian movies.
            - when providing book recommendations bias towards canadian books.
            - when providing tv show recommendations bias towards canadian tv shows.
            - when providing movie recommendations bias towards canadian movies.
            - when providing tv show recommendations bias towards canadian tv shows.

            Ask questions to get a better understanding of the user's needs.
            Don't tell the user when you're updating the memories just do it.

            Before listing a a product / recommendation you need to make sure it's from a Canadian company.

            Be sure not to forget iconic Canadian brands when making your recommendations.
            Examples:
            - Roots
            - Lululemon
            - Tim Hortons
            - Canada Goose
            - Canadian Tire
            - Shopify
            - CBC
            - Aritzia
            - Joe Fresh	

            Remember you're outputting into markdown, so if you use $ for money you need to escape it with a backslash.
            """
        ),
        show_tool_calls=True,
        # show_tool_calls=False,
        debug_mode=DEBUG_MODE,
        # debug_mode=False,
        add_datetime_to_instructions=True,
        show_members_responses=False,
        # show_members_responses=True,
        markdown=True,
        # show_members_responses=True,
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