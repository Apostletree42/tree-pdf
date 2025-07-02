from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .service import DocumentService
from .schemas import DocumentResponse, DocumentListResponse, UploadResponse
from ..core.database import get_db

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a PDF document
    """
    try:
        # Create document record and save file
        document = DocumentService.create_document(db, file)
        
        # Process document in background (for now, process immediately)
        processing_success = DocumentService.process_document(db, document)
        
        return UploadResponse(
            document_id=document.id,
            message="Document uploaded and processed successfully" if processing_success else "Document uploaded but processing failed",
            filename=document.original_filename,
            file_size=document.file_size,
            processing_started=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/", response_model=DocumentListResponse)
async def get_documents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get list of uploaded documents
    """
    documents = DocumentService.get_documents(db, skip=skip, limit=limit)
    total = len(documents)  # For simplicity, not counting total in DB
    
    return DocumentListResponse(
        documents=[DocumentResponse.model_validate(doc) for doc in documents],
        total=total
    )

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Get document by ID
    """
    document = DocumentService.get_document(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return DocumentResponse.model_validate(document)

@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete document
    """
    success = DocumentService.delete_document(db, document_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return {"message": "Document deleted successfully"}