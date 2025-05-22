from fastmcp import FastMCP

from src.config import config
from src.docs import search_relevant_docs

mcp = FastMCP("SecondBrain", host="0.0.0.0", port=8000)


@mcp.tool()
def get_documents(query: str) -> list[str]:
    """Retrieves most relevant documents from vector database."""
    return search_relevant_docs(query, config.DOCS_SEARCH_N_RESULTS)


mcp.run("streamable-http")
