import http.client
import json
import os
from dotenv import load_dotenv
import httpx 
import asyncio
from fastmcp import FastMCP
from utils import clean_html

# Load variables from .env into the environment
load_dotenv()
mcp = FastMCP("Official docs")

query="langchain chroma db"
serper_url = "https://google.serper.dev/search"

async def web_search(query: str) -> dict | None:
    payload = json.dumps({"q": query,"num": 3})
    headers = {
    'X-API-KEY': os.getenv('SERPER_API_KEY'),
    'Content-Type': 'application/json'
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=serper_url, 
            data=payload, 
            headers=headers,
            timeout=30.0)
        return response.json()
    # conn = http.client.HTTPSConnection("google.serper.dev")
    # conn.request("POST", "/search", payload, headers)
    # res = conn.getresponse()
    # data = res.read()
    # return {data.decode("utf-8")}


# step 2: open official documentation
async def fetch_url(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=30.0)
        cleaned_response = clean_html(response.text)
        return cleaned_response

official_docs = {
    "langchain": "docs.langchain.com/",
    "llama-index": "docs.llamaindex.ai/en/stable",
    "openai": "platform.openai.com/docs",
    "uv": "docs.astral.sh/uv",
}

@mcp.tool
async def get_docs(query: str, library: str):
    """
    Search the latest docs for a given query and library.
    Supports langchain, openai, llama-index and uv.

    Args:
        query: The query to search for (e.g. "Publish a package with UV")
        library: The library to search in (e.g. "uv")

    Returns:
        Summarized text from the docs with source links.
    """
    if library not in official_docs:
        raise ValueError(f"Library {library} not supported!")

    query = f"site:{official_docs[library]} {query}"

    response = await web_search(query)
    if len(response['organic']) == 0:
        return "No results found"

    text_parts = []
    for res in response['organic']:
        link = res.get("link", "")
        raw = await fetch_url(link)
        if raw:
            labeled = f"SOURCE: {link}\n{raw}"
            text_parts.append(labeled)


    return "\n\n".join(text_parts)


def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()