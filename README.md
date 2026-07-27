# MCP Docs Assistant

A Python MCP project that exposes documentation retrieval as a tool and demonstrates how an agentic LLM client can use that tool to answer developer questions with fetched source context.

The main workflow runs an MCP server over stdio, searches supported official documentation sites through Serper, extracts readable page content, and passes the retrieved context to a Groq-hosted LLM for a grounded response. The repository also includes a small context-sharing MCP server example for storing and retrieving agent context in memory.

## Key Features

- MCP stdio server with a `get_docs` tool for documentation lookup.
- Search constrained to supported official docs: LangChain, LlamaIndex, OpenAI, and uv.
- Async HTTP fetching with `httpx` and cleaned page extraction via `trafilatura`.
- Example MCP client that discovers tools, calls the server, and sends retrieved context to Groq.
- Simple agentic workflow pattern: discover a tool, retrieve external context, then generate a grounded answer.
- Separate context-sharing server example with tools for `share_context`, `retrieve_context`, and `list_all_context`.

## Tech Stack

- Python
- MCP / FastMCP
- httpx
- python-dotenv
- Serper API
- Groq API
- trafilatura

## Project Structure

```text
.
|-- mcp_server.py                    # Main docs-retrieval MCP server
|-- client.py                        # Example MCP client and LLM response flow
|-- utils.py                         # HTML cleanup and Groq completion helper
|-- mcp-context-sharing/
|   `-- src/server/main.py           # In-memory context-sharing MCP server example
|-- requirements.txt                 # Python dependency snapshot
|-- .env.example                     # Required environment variables
`-- pyproject.toml                   # Placeholder project metadata
```

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
pip install fastmcp groq trafilatura
```

Create a local environment file:

```bash
copy .env.example .env
```

Then add API keys:

```env
SERPER_API_KEY=your_serper_api_key
GROQ_API_KEY=your_groq_api_key
```

## Run Locally

Run the example client, which starts `mcp_server.py` over stdio, lists available tools, calls `get_docs`, and asks Groq to answer from the returned context:

```bash
python client.py
```

Run the docs server directly:

```bash
python mcp_server.py
```

Run the context-sharing server example:

```bash
python mcp-context-sharing/src/server/main.py
```

## Usage Flow

1. `client.py` starts the MCP server with stdio transport.
2. The client initializes an MCP session and lists available tools.
3. It calls `get_docs` with a developer query and supported library name.
4. `mcp_server.py` searches the relevant official docs domain through Serper.
5. Matching pages are fetched, cleaned, labeled with source URLs, and returned.
6. The client sends the retrieved context to Groq and prints the answer.

Supported library values:

```text
langchain
llama-index
openai
uv
```

## Testing and Build

No automated test suite or build pipeline is currently defined. For a smoke test, configure the environment variables and run:

```bash
python client.py
```

## Deployment Notes

The current implementation is designed for local MCP stdio execution. It does not include a hosted API service, persistent storage layer, or production deployment configuration.

## Future Scope

- Add tests around tool behavior, error handling, and response shaping.
- Move supported docs sources into configuration.
- Add caching or persistence for fetched documentation.
- Package the server with complete dependency metadata in `pyproject.toml`.
