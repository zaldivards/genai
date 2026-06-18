from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from agent.graph import graph

router = APIRouter(prefix="/agent", tags=["agent"])


class ChatInput(BaseModel):
    message: str
    thread_id: str


class ChatOutput(BaseModel):
    response: str
    thread_id: str


@router.post("/chat")
async def chat_with_agent(input_: ChatInput):
    try:
        config = {"configurable": {"thread_id": input_.thread_id}}
        state = {"messages": [{"role": "user", "content": input_.message}]}
        result = await graph.ainvoke(state, config=config)
        return ChatOutput(
            response=result["messages"][-1].content, thread_id=input_.thread_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e
