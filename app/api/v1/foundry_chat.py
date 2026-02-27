from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.services.foundry_chat_service import chat_with_foundry_agent

router = APIRouter(prefix="/api/v1/foundry", tags=["foundry"])


class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    response: Dict[str, Any]


@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """
    Send a message to the Foundry Agent and receive a response.
    
    Args:
        request: ChatRequest containing message and optional context
        
    Returns:
        ChatResponse containing the agent's response
    """
    response = await chat_with_foundry_agent(
        message=request.message,
        context=request.context
    )
    
    return ChatResponse(response=response)
