import os
import uuid
from datetime import datetime
from typing import Optional, List
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
import fitz  # PyMuPDF

from .models import Document
from .schemas import DocumentCreate, DocumentResponse
from ..core.config import settings
from ..rag.vector_store import get_vector_store
from ..rag.text_processing import chunk_text

class DocumentService:
    
    @staticmethod
    def save_uploaded_file(file: UploadFile) -> tuple[str, int]:
        """
        Save uploaded file to storage directory
        
        Returns:
            tuple: (file_path, file_size)
        """
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = f"{settings.storage_path}/uploads/{unique_filename}"
        
        # Save file
        try:
            with open(file_path, "wb") as buffer:
                content = file.file.read()
                buffer.write(content)
                file_size = len(content)
            
            print(f"✅ Saved file: {file_path} ({file_size} bytes)")
            return file_path, file_size
            
        except Exception as e:
            print(f"❌ Error saving file: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> tuple[str, int]:
        """
        Extract text from PDF using PyMuPDF
        
        Returns:
            tuple: (extracted_text, page_count)
        """
        try:
            doc = fitz.open(file_path)
            text_content = ""
            page_count = len(doc)  # Get page count before processing
            
            for page_num in range(page_count):
                page = doc.load_page(page_num)
                text_content += page.get_text()
                text_content += "\n\n"  # Add page separator
            
            doc.close()
            
            print(f"✅ Extracted text from PDF: {len(text_content)} characters, {page_count} pages")
            return text_content.strip(), page_count
            
        except Exception as e:
            print(f"❌ Error extracting text from PDF: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to extract text from PDF: {str(e)}")
    
    @staticmethod
    def process_document(db: Session, document: Document) -> bool:
        """
        Process document: extract text, create chunks, build vector index
        
        Returns:
            bool: Success status
        """
        try:
            # Extract text from PDF
            text_content, page_count = DocumentService.extract_text_from_pdf(document.file_path)
            
            if not text_content.strip():
                raise ValueError("No text content found in PDF")
            
            # Create text chunks
            chunks = chunk_text(text_content, chunk_size=500, overlap=50)
            
            if not chunks:
                raise ValueError("No text chunks created")
            
            # Create vector index
            vector_store = get_vector_store(document.id)
            vector_store.create_index(chunks)
            
            # Update document metadata
            document.processed = True
            document.processing_error = None
            document.chunk_count = len(chunks)
            document.total_pages = page_count
            document.total_characters = len(text_content)
            document.processed_date = datetime.utcnow()
            
            db.commit()
            
            print(f"✅ Successfully processed document {document.id}: {len(chunks)} chunks created")
            return True
            
        except Exception as e:
            # Update document with error
            document.processed = False
            document.processing_error = str(e)
            db.commit()
            
            print(f"❌ Error processing document {document.id}: {e}")
            return False
    
    @staticmethod
    def create_document(db: Session, file: UploadFile) -> Document:
        """
        Create new document record and save file
        """
        # Validate file
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        if file.size and file.size > settings.upload_max_size:
            raise HTTPException(status_code=400, detail=f"File too large. Max size: {settings.upload_max_size} bytes")
        
        # Save file
        file_path, file_size = DocumentService.save_uploaded_file(file)
        
        # Create database record
        document_data = DocumentCreate(
            filename=os.path.basename(file_path),
            original_filename=file.filename,
            file_path=file_path,
            file_size=file_size
        )
        
        document = Document(**document_data.dict())
        db.add(document)
        db.commit()
        db.refresh(document)
        
        return document
    
    @staticmethod
    def get_document(db: Session, document_id: int) -> Optional[Document]:
        """Get document by ID"""
        return db.query(Document).filter(Document.id == document_id).first()
    
    @staticmethod
    def get_documents(db: Session, skip: int = 0, limit: int = 100) -> List[Document]:
        """Get list of documents"""
        return db.query(Document).offset(skip).limit(limit).all()
    
    @staticmethod
    def delete_document(db: Session, document_id: int) -> bool:
        """Delete document and associated files"""
        document = DocumentService.get_document(db, document_id)
        if not document:
            return False
        
        try:
            # Delete vector index
            vector_store = get_vector_store(document_id)
            vector_store.delete()
            
            # Delete file
            if os.path.exists(document.file_path):
                os.remove(document.file_path)
            
            # Delete database record
            db.delete(document)
            db.commit()
            
            print(f"✅ Deleted document {document_id}")
            return True
            
        except Exception as e:
            print(f"❌ Error deleting document {document_id}: {e}")
            return False