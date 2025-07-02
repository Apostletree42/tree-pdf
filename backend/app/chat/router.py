from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .service import ChatService
from .schemas import QuestionRequest, QuestionResponse, ConversationHistoryResponse, ConversationResponse
from ..documents.service import DocumentService
from ..core.database import get_db

router = APIRouter()

@router.post("/ask", response_model=QuestionResponse)
async def ask_question(
    request: QuestionRequest,
    db: Session = Depends(get_db)
):
    """
    Ask a question about a document
    """
    return ChatService.ask_question(db, request)

@router.get("/history/{document_id}", response_model=ConversationHistoryResponse)
async def get_conversation_history(
    document_id: int,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Get conversation history for a document
    """
    document = DocumentService.get_document(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    conversations = ChatService.get_conversation_history(db, document_id, limit)
    
    return ConversationHistoryResponse(
        conversations=[ConversationResponse.model_validate(conv) for conv in conversations],
        total=len(conversations),
        document_filename=document.original_filename
    )

@router.get("/conversation/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific conversation by ID
    """
    conversation = ChatService.get_conversation(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return ConversationResponse.model_validate(conversation)