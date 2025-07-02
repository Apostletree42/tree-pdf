from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class QuestionRequest(BaseModel):
    document_id: int
    question: str

class QuestionResponse(BaseModel):
    answer: str
    question: str
    document_id: int
    context_chunks_used: int
    response_time_seconds: float
    conversation_id: int

class ConversationResponse(BaseModel):
    id: int
    document_id: int
    question: str
    answer: str
    context_chunks_used: int
    response_time_seconds: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True

class ConversationHistoryResponse(BaseModel):
    conversations: List[ConversationResponse]
    total: int
    document_filename: Optional[str] = None