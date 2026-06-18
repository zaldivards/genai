from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI

from agent.tools import search_docs

tools = [search_docs]

llm = ChatOpenAI(model="gpt-4", temperature=0).bind_tools(tools)


async def agent(state: MessagesState):
    return {"messages": await llm.ainvoke(state["messages"])}


builder = StateGraph(MessagesState)


builder.add_node("agent", agent)
builder.add_node("tools", ToolNode(tools))
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")
builder.set_entry_point("agent")

graph = builder.compile(checkpointer=MemorySaver())
