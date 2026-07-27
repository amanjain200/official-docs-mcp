import asyncio

import os
from dotenv import load_dotenv

from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client
from mcp import StdioServerParameters

from groq import Groq

from utils import get_response_from_llm


load_dotenv()



server_params = StdioServerParameters(
    command= "python",
    args=["mcp_server.py"],
    env = None
)


async def main():
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools_response = await session.list_tools()
            print("availalble tools: ", {t.name for t in tools_response.tools})

            query = "How to use chromadb with langchain"
            library = "langchain"
            res = await session.call_tool("get_docs", arguments ={"query": query, "library": library})

            context = res.content

            USER_PROMPT = f"Query: {query}, \n Context: {context}"


            # LLM call to create readable output
            SYSTEM_PROMPT = """
            USE ONLY THP PROVIDED CONTEXT TO ANSWER THE USER QUERY. If info is missing say you don't know.
            Keep every 'SOURCE:' line exactly; list sources at the end.
            """

            ans = get_response_from_llm(
                user_prompt=USER_PROMPT,
                system_prompt=SYSTEM_PROMPT,
                model="openai/gpt-oss-120b"
            )

            print(ans)


if __name__ == "__main__":
    asyncio.run(main())