from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey('documents.id'), nullable=False)
    
    # Question and Answer
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    
    # Context and metadata
    context_chunks_used = Column(Integer, default=0)
    response_time_seconds = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, document_id={self.document_id}, question='{self.question[:50]}...')>"