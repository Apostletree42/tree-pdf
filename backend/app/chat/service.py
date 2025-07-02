import os
import time
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from fastapi import HTTPException
import google.generativeai as genai

from .models import Conversation
from .schemas import QuestionRequest, QuestionResponse, ConversationResponse
from ..documents.service import DocumentService
from ..rag.vector_store import get_vector_store
from ..core.config import settings

# Configure Gemini
genai.configure(api_key=settings.gemini_api_key)

class ChatService:
    
    @staticmethod
    def _get_gemini_model():
        """Get Gemini model instance"""
        try:
            model_name = os.environ.get("MODEL_NAME", "gemini-2.0-flash-001")
            model = genai.GenerativeModel(model_name)
            return model
        except Exception as e:
            print(f"❌ Error initializing Gemini model: {e}")
            raise HTTPException(status_code=500, detail="Failed to initialize AI model")
    
    @staticmethod
    def _retrieve_relevant_context(document_id: int, question: str, top_k: int = 5) -> Tuple[List[str], int]:
        """
        Retrieve relevant context chunks for the question
        
        Returns:
            tuple: (context_chunks, chunks_count)
        """
        try:
            vector_store = get_vector_store(document_id)
            if not vector_store.exists():
                raise ValueError(f"No vector index found for document {document_id}")

            search_results = vector_store.search(question, top_k=top_k)

            context_chunks = [text for text, score in search_results]

            return context_chunks, len(context_chunks)
            
        except Exception as e:
            print(f"❌ Error retrieving context: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to retrieve context: {str(e)}")
    
    @staticmethod
    def _generate_answer(question: str, context_chunks: List[str]) -> str:
        """
        Generate answer using Gemini with retrieved context
        """
        try:
            context_text = "\n\n".join([f"Context {i+1}: {chunk}" for i, chunk in enumerate(context_chunks)])

            prompt = f"""Based on the following context from a document, please answer the question. If the answer cannot be found in the context, please say so clearly.

Context:
{context_text}

Question: {question}

Please provide a comprehensive answer based on the context above. If specific information is not available in the context, mention that clearly."""

            model = ChatService._get_gemini_model()
            response = model.generate_content(prompt)
            
            if not response.text:
                return "I apologize, but I couldn't generate a response. Please try rephrasing your question."
            return response.text.strip()
            
        except Exception as e:
            print(f"Error generating answer: {e}")
            return f"I apologize, but I encountered an error while processing your question: {str(e)}. Please try again."
    
    @staticmethod
    def ask_question(db: Session, request: QuestionRequest) -> QuestionResponse:
        """
        Process a question and return an answer
        """
        start_time = time.time()
        
        # Validate document exists and is processed
        document = DocumentService.get_document(db, request.document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        if not document.processed:
            raise HTTPException(status_code=400, detail="Document is not yet processed")
        
        try:
            # Retrieve relevant context
            context_chunks, chunks_used = ChatService._retrieve_relevant_context(
                request.document_id, 
                request.question,
                top_k=5
            )
            
            # Generate answer
            answer = ChatService._generate_answer(request.question, context_chunks)
            
            # Calculate response time
            response_time = time.time() - start_time
            
            # Save conversation to database
            conversation = Conversation(
                document_id=request.document_id,
                question=request.question,
                answer=answer,
                context_chunks_used=chunks_used,
                response_time_seconds=response_time
            )
            
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            
            # print(f"Successfully processed question for document {request.document_id}")
            
            return QuestionResponse(
                answer=answer,
                question=request.question,
                document_id=request.document_id,
                context_chunks_used=chunks_used,
                response_time_seconds=response_time,
                conversation_id=conversation.id
            )
            
        except HTTPException:
            raise
        except Exception as e:
            print(f"Error processing question: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to process question: {str(e)}")
    
    @staticmethod
    def get_conversation_history(db: Session, document_id: int, limit: int = 50) -> List[Conversation]:
        """
        Get conversation history for a document
        """
        try:
            conversations = (
                db.query(Conversation)
                .filter(Conversation.document_id == document_id)
                .order_by(Conversation.created_at.desc())
                .limit(limit)
                .all()
            )
            
            return conversations
            
        except Exception as e:
            print(f"Error getting conversation history: {e}")
            raise HTTPException(status_code=500, detail="Failed to get conversation history")
    
    @staticmethod
    def get_conversation(db: Session, conversation_id: int) -> Optional[Conversation]:
        """Get single conversation by ID"""
        return db.query(Conversation).filter(Conversation.id == conversation_id).first()