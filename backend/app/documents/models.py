from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from ..core.database import Base

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    
    # Processing status
    processed = Column(Boolean, default=False, nullable=False)
    processing_error = Column(Text, nullable=True)
    chunk_count = Column(Integer, default=0)
    
    # Timestamps
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    processed_date = Column(DateTime(timezone=True), nullable=True)
    
    # Content metadata
    total_pages = Column(Integer, nullable=True)
    total_characters = Column(Integer, nullable=True)
    
    def __repr__(self):
        return f"<Document(id={self.id}, filename='{self.filename}', processed={self.processed})>"