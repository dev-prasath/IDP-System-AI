from fastapi import APIRouter, HTTPException

from backend.chatbot.chat_schema import ChatRequest
from backend.chatbot.session_manager import session_manager

router = APIRouter()


@router.post("/chat-document")
async def chat_document(request: ChatRequest):

    chatbot = session_manager.get_session(
        request.document_id
    )

    if chatbot is None:

        raise HTTPException(
            status_code=404,
            detail="Document session not found."
        )

    answer = chatbot.ask(
        request.question
    )

    return {
        "success": True,
        "answer": answer
    }