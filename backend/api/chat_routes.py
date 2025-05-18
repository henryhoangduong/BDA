from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

from services.chatbots.chat4u.state import State

chat = APIRouter()


# request input format
class Query(BaseModel):
    message: str


class Query(BaseModel):
    message: str


@chat.post("/chat")
async def invoke_graph(query: Query = Body(...)):
    config = {"configurable": {"thread_id":"2"}}
    state=State()
    state["messages"] = [HumanMessage(content=query.message)]

    def is_numeric(s):
        import re
        return bool(re.match(r'^[\d ]+$', s.strip()))
    
    # async for event in graph.