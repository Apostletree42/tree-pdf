from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentBase(BaseModel):
    filename: str
    original_filename: str

class DocumentCreate(DocumentBase):
    file_path: str
    file_size: int

class DocumentResponse(DocumentBase):
    id: int
    file_size: int
    processed: bool
    processing_error: Optional[str] = None
    chunk_count: int
    upload_date: datetime
    processed_date: Optional[datetime] = None
    total_pages: Optional[int] = None
    total_characters: Optional[int] = None
    
    class Config:
        from_attributes = True

class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]
    total: int

class UploadResponse(BaseModel):
    document_id: int
    message: str
    filename: str
    file_size: int
    processing_started: bool