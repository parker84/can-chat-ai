# tools.py
from agno.tools import tool
import os
import httpx
import asyncio
from typing import List, Dict, Tuple
from urllib.parse import quote

# ---------- Shared HTTP client (HTTP/2 + pooling) ----------
_http_client: httpx.AsyncClient | None = None
_client_lock = asyncio.Lock()

async def get_client() -> httpx.AsyncClient:
    """
    Create (once) and reuse a single HTTP/2 AsyncClient for all tools.
    Reuse avoids repeated TCP/TLS handshakes and enables multiplexing.
    """
    global _http_client
    if _http_client is None:
        async with _client_lock:
            if _http_client is None:
                _http_client = httpx.AsyncClient(
                    http2=True,
                    timeout=httpx.Timeout(20.0),
                    limits=httpx.Limits(
                        max_connections=100,
                        max_keepalive_connections=20,
                    ),
                    headers={"x-puremd-api-token": os.environ.get("PUREMD_API_KEY")}
                )
    return _http_client


# =========================
# Single-item tools
# =========================

@tool(cache_results=True, cache_dir="/tmp/agno_cache", cache_ttl=60*60)
async def fetch_url_contents(url: str = '') -> str:
    """
    Fetch the contents (HTML or text) of a single URL.

    WHEN TO USE
    - You only need ONE page, or you already have the exact page to fetch.
    - If you need MULTIPLE pages, **prefer `fetch_urls`** (the batch tool) to save time.

    ARGS
    - url (str): Relative or absolute path to fetch (e.g., "article/123" or "https://...").

    RETURNS
    - str: Raw response text. Empty string on non-200 or invalid input.

    EXAMPLES
    - Use for a single detail page you’re certain about.
    - If you need to fetch 3–10 pages, **use `fetch_urls` instead**.
    """
    if isinstance(url, str) and url.strip():
        client = await get_client()
        r = await client.get(f'https://pure.md/{url}')
        if r.status_code == 200:
            return r.text
    return ""


@tool(cache_results=True, cache_dir="/tmp/agno_cache", cache_ttl=60*60)
async def search_web(query: str = '') -> str:
    """
    Run a single web search query.

    WHEN TO USE
    - You only need ONE query.
    - If you need multiple related queries, **prefer `search_web_multi`** (batch) to reduce latency.

    ARGS
    - query (str): A clear, specific search term or question.

    RETURNS
    - str: Raw JSON/text from the search endpoint. Empty string on error/invalid input.

    EXAMPLES
    - ONE query to orient yourself.
    - For 2+ queries (e.g., brand variations, model comparisons), **use `search_web_multi`** instead.
    """
    if isinstance(query, str) and query.strip():
        client = await get_client()
        r = await client.get(f'https://pure.md/search?q={quote(query)}')
        r.raise_for_status()
        return r.text
    return ""


# =========================
# Batch tools (prefer these)
# =========================

# Optional: cap parallelism to avoid over-fan-out
_MAX_PARALLEL = int(os.environ.get("BATCH_MAX_PARALLEL", "10"))
_semaphore = asyncio.Semaphore(_MAX_PARALLEL)

@tool(cache_results=True, cache_dir="/tmp/agno_cache", cache_ttl=60*60)
async def fetch_urls(urls: List[str]) -> Dict[str, str]:
    """
    Fetch multiple URLs **in parallel** (fast path). Prefer this over repeated `fetch_url_contents`.

    WHEN TO USE
    - You need to read **several** pages (e.g., product pages, brand sites, reviews).
    - You already have a candidate list of URLs, or you’re expanding coverage quickly.

    ARGS
    - urls (List[str]): A list of relative or absolute URLs. Empty/invalid items are ignored.

    RETURNS
    - Dict[str, str]: A mapping of `url -> response_text` (empty string if failed).

    BEHAVIOR & PERFORMANCE
    - Uses a shared HTTP/2 client and parallelizes with `asyncio.gather`.
    - Rate-limited by a semaphore (default 10 concurrent). Tune via env `BATCH_MAX_PARALLEL`.

    MODEL GUIDANCE
    - If you’re about to call `fetch_url_contents` multiple times, **combine them into one**
      `fetch_urls([...])` call instead.
    - Keep lists reasonable (≤ 10–15) unless strictly necessary.

    EXAMPLE
    >>> await fetch_urls([
    ...   "canadian-brands/umbrellas/midtown",
    ...   "https://pure.md/canadian-brands/umbrellas/vancouver-umbrella",
    ... ])
    """
    client = await get_client()

    async def one(u: str) -> Tuple[str, str]:
        if not isinstance(u, str) or not u.strip():
            return (u, "")
        try:
            async with _semaphore:
                r = await client.get(f'https://pure.md/{u}')
            return (u, r.text if r.status_code == 200 else "")
        except Exception:
            return (u, "")

    # Small safety: de-dup to avoid wasted calls
    dedup = list(dict.fromkeys(urls or []))[:50]  # hard ceiling, adjust if needed
    results = await asyncio.gather(*[one(u) for u in dedup], return_exceptions=False)
    return {u: text for (u, text) in results}


@tool(cache_results=True, cache_dir="/tmp/agno_cache", cache_ttl=60*60)
async def search_web_multi(queries: List[str]) -> Dict[str, str]:
    """
    Run multiple web search queries **in parallel** (fast path). Prefer this over repeated `search_web`.

    WHEN TO USE
    - You need **several** related queries (brand variations, “made in Canada” checks, model families).
    - You’re compiling options and want coverage quickly before filtering.

    ARGS
    - queries (List[str]): A list of search strings. Empty/invalid items are ignored.

    RETURNS
    - Dict[str, str]: A mapping of `query -> raw_search_response_text` (empty string if failed).

    BEHAVIOR & PERFORMANCE
    - Uses a shared HTTP/2 client and parallelization with a concurrency cap (default 10).
    - This minimizes round-trips compared to serial tool calls.

    MODEL GUIDANCE
    - If you’re planning to call `search_web` multiple times in a row, **batch them** into a single
      `search_web_multi([...])` call.
    - After getting results, extract/score the best candidates, then (optionally) call `fetch_urls`
      **once** to pull the details.

    EXAMPLE
    >>> await search_web_multi([
    ...   "Top Canadian umbrella brands",
    ...   "Midtown Umbrellas warranty",
    ...   "Vancouver Umbrella made in Canada",
    ... ])
    """
    client = await get_client()

    async def one(q: str) -> Tuple[str, str]:
        if not isinstance(q, str) or not q.strip():
            return (q, "")
        try:
            async with _semaphore:
                r = await client.get(f'https://pure.md/search?q={quote(q)}')
            r.raise_for_status()
            return (q, r.text)
        except Exception:
            return (q, "")

    # Small safety: de-dup to avoid wasted calls
    dedup = list(dict.fromkeys(queries or []))[:50]  # hard ceiling, adjust if needed
    results = await asyncio.gather(*[one(q) for q in dedup], return_exceptions=False)
    return {q: text for (q, text) in results}
