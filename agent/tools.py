from langchain_core.tools import tool

from agent.vectorstore import vectorstore


@tool
def search_docs(query: str):
    """Search the BEON docs for relevant documents."""
    results = vectorstore.similarity_search(query, k=5)
    return "\n\n".join([r.page_content for r in results])
