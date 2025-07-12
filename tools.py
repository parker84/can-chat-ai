from agno.tools import tool
import os
import httpx
from urllib.parse import quote

# @tool(
#     cache_results=True,                             # Enable caching of results
#     cache_dir="/tmp/agno_cache",                    # Custom cache directory
#     cache_ttl=60*60                                  # Cache TTL in seconds (1 hour)
# )
# # async def fetch_url_contents(url: str = '') -> str:
# async def fetch_url_contents(url: str = '') -> str:
#     """
#     Fetch the contents of a given URL and return its full HTML or textual content.
#     This is used to understand linked content so the email can reflect it properly.

#     Args:
#         url: The URL (relative path or full) to fetch content from. Defaults to ''.

#     Returns:
#         str: The content of the fetched URL, used to help write a personalized and accurate email.
#     """
#     if isinstance(url, str):
#         if url.strip():
#             headers = {"x-puremd-api-token": os.environ.get("PUREMD_API_KEY")}
#             async with httpx.AsyncClient(timeout=20) as client:
#                 response = await client.get(f'https://pure.md/{url}', headers=headers)
#                 if response.status_code == 200:
#                     return response.text
#     return ""

# @tool(
#     cache_results=True,                             # Enable caching of results
#     cache_dir="/tmp/agno_cache",                    # Custom cache directory
#     cache_ttl=60*60                                  # Cache TTL in seconds (1 hour)
# )
# async def search_web(query: str = '') -> str:
#     """
#     This tool should be used when you need to:
#     - Find current information or real-time data from the web
#     - Get facts, news, or knowledge that might not be in your training data
#     - Research answers to specific questions by querying the internet
#     - Access web content like articles, documentation, or reference materials

#     Args:
#         query (str): The search query or question to look up on the internet. This should
#                 be a clear, specific search term or question that will yield relevant results.

#     Returns:
#         str: A list of search results, where each result contains:
#                 - url: URL of the webpage containing the information
#                 - title: Title of the webpage
#                 - description: Brief description of the webpage content
#                 - access_date: Date when the webpage was last accessed
#                 - current_date: Current date when the search was performed
#                 - snippet: Brief excerpt/description of the content

#     Example:
#         results = await search_web("latest AI developments 2025")
#         # Returns list of relevant web pages about recent AI progress
#     """
#     if isinstance(query, str):
#         if query.strip():
#             headers = {"x-puremd-api-token": os.environ.get("PUREMD_API_KEY")}
#             async with httpx.AsyncClient(timeout=20) as client:
#                 response = await client.get(f'https://pure.md/search?q={quote(query)}', headers=headers)
#                 response.raise_for_status()
#                 return response.text
#     return ""

# TODO: make it async
@tool(
    cache_results=True,                             # Enable caching of results
    cache_dir="/tmp/agno_cache",                    # Custom cache directory
    cache_ttl=60*60                                  # Cache TTL in seconds (1 hour)
)
def fetch_url_contents(url: str = '') -> str:
    """
    Fetch the contents of a given URL and return its full HTML or textual content.
    This is used to understand linked content so the email can reflect it properly.

    Args:
        url: The URL (relative path or full) to fetch content from. Defaults to ''.

    Returns:
        str: The content of the fetched URL, used to help write a personalized and accurate email.
    """
    if isinstance(url, str):
        if url.strip():
            headers = {"x-puremd-api-token": os.environ.get("PUREMD_API_KEY")}
            with httpx.Client(timeout=20) as client:
                response = client.get(f'https://pure.md/{url}', headers=headers)
                if response.status_code == 200:
                    return response.text
    return ""

@tool(
    cache_results=True,                             # Enable caching of results
    cache_dir="/tmp/agno_cache",                    # Custom cache directory
    cache_ttl=60*60                                  # Cache TTL in seconds (1 hour)
)
def search_web(query: str = '') -> str:
    """
    This tool should be used when you need to:
    - Find current information or real-time data from the web
    - Get facts, news, or knowledge that might not be in your training data
    - Research answers to specific questions by querying the internet
    - Access web content like articles, documentation, or reference materials

    Args:
        query (str): The search query or question to look up on the internet. This should
                be a clear, specific search term or question that will yield relevant results.

    Returns:
        str: A list of search results, where each result contains:
                - url: URL of the webpage containing the information
                - title: Title of the webpage
                - description: Brief description of the webpage content
                - access_date: Date when the webpage was last accessed
                - current_date: Current date when the search was performed
                - snippet: Brief excerpt/description of the content

    Example:
        results = await search_web("latest AI developments 2025")
        # Returns list of relevant web pages about recent AI progress
    """
    if isinstance(query, str):
        if query.strip():
            headers = {"x-puremd-api-token": os.environ.get("PUREMD_API_KEY")}
            with httpx.Client(timeout=20) as client:
                response = client.get(f'https://pure.md/search?q={quote(query)}', headers=headers)
                response.raise_for_status()
                return response.text
    return ""