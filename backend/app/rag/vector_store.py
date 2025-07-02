import faiss
import numpy as np
import pickle
import os
from typing import List, Tuple, Optional
from ..core.config import settings
from .embeddings import embedding_service

class VectorStore:
    def __init__(self, document_id: int):
        self.document_id = document_id
        self.index = None
        self.texts = []
        self.embedding_dim = embedding_service.get_embedding_dimension()
        
        # File paths
        self.index_path = f"{settings.storage_path}/indexes/doc_{document_id}.index"
        self.texts_path = f"{settings.storage_path}/indexes/doc_{document_id}_texts.pkl"
    
    def create_index(self, texts: List[str]) -> None:
        """
        Create FAISS index from text chunks
        
        Args:
            texts: List of text chunks to index
        """
        if not texts:
            raise ValueError("No texts provided to create index")
        
        try:
            # Create embeddings
            embeddings = embedding_service.create_embeddings(texts)
            
            # Create FAISS index
            self.index = faiss.IndexFlatL2(self.embedding_dim)
            self.index.add(embeddings.astype('float32'))
            
            # Store texts for retrieval
            self.texts = texts
            
            # Save to disk
            self._save_index()
            
            print(f"✅ Created vector index for document {self.document_id} with {len(texts)} chunks")
            
        except Exception as e:
            print(f"❌ Error creating vector index: {e}")
            raise e
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Search for similar text chunks
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of (text, similarity_score) tuples
        """
        if not self.index:
            self._load_index()
        
        if not self.index:
            raise ValueError("No index found. Create index first.")
        
        try:
            # Create query embedding
            query_embedding = embedding_service.create_single_embedding(query)
            query_embedding = query_embedding.reshape(1, -1).astype('float32')
            
            # Search
            distances, indices = self.index.search(query_embedding, min(top_k, len(self.texts)))
            
            # Format results
            results = []
            for distance, idx in zip(distances[0], indices[0]):
                if idx < len(self.texts):  # Valid index
                    similarity_score = 1 / (1 + distance)  # Convert distance to similarity
                    results.append((self.texts[idx], similarity_score))
            
            print(f"✅ Found {len(results)} similar chunks for query")
            return results
            
        except Exception as e:
            print(f"❌ Error searching vector index: {e}")
            raise e
    
    def _save_index(self) -> None:
        """Save FAISS index and texts to disk"""
        try:
            # Save FAISS index
            faiss.write_index(self.index, self.index_path)
            
            # Save texts
            with open(self.texts_path, 'wb') as f:
                pickle.dump(self.texts, f)
                
            print(f"✅ Saved vector index to {self.index_path}")
            
        except Exception as e:
            print(f"❌ Error saving vector index: {e}")
            raise e
    
    def _load_index(self) -> bool:
        """Load FAISS index and texts from disk"""
        try:
            if os.path.exists(self.index_path) and os.path.exists(self.texts_path):
                # Load FAISS index
                self.index = faiss.read_index(self.index_path)
                
                # Load texts
                with open(self.texts_path, 'rb') as f:
                    self.texts = pickle.load(f)
                
                print(f"✅ Loaded vector index from {self.index_path}")
                return True
            else:
                print(f"⚠️ Vector index not found for document {self.document_id}")
                return False
                
        except Exception as e:
            print(f"❌ Error loading vector index: {e}")
            return False
    
    def exists(self) -> bool:
        """Check if vector index exists for this document"""
        return os.path.exists(self.index_path) and os.path.exists(self.texts_path)
    
    def delete(self) -> None:
        """Delete vector index files"""
        try:
            if os.path.exists(self.index_path):
                os.remove(self.index_path)
            if os.path.exists(self.texts_path):
                os.remove(self.texts_path)
            print(f"✅ Deleted vector index for document {self.document_id}")
        except Exception as e:
            print(f"❌ Error deleting vector index: {e}")

def get_vector_store(document_id: int) -> VectorStore:
    """Factory function to get vector store for a document"""
    return VectorStore(document_id)