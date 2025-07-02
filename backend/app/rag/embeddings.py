from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np
from ..core.config import settings

class EmbeddingService:
    def __init__(self):
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the sentence transformer model"""
        try:
            print(f"Loading embedding model: {settings.embedding_model}")
            self.model = SentenceTransformer(settings.embedding_model)
            print("✅ Embedding model loaded successfully")
        except Exception as e:
            print(f"❌ Error loading embedding model: {e}")
            raise e
    
    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Create embeddings for a list of texts
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            numpy array of embeddings
        """
        if not texts:
            return np.array([])
        
        try:
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            print(f"✅ Created embeddings for {len(texts)} text chunks")
            return embeddings
        except Exception as e:
            print(f"❌ Error creating embeddings: {e}")
            raise e
    
    def create_single_embedding(self, text: str) -> np.ndarray:
        """
        Create embedding for a single text
        
        Args:
            text: Text string to embed
            
        Returns:
            numpy array embedding
        """
        return self.create_embeddings([text])[0]
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings from this model"""
        return self.model.get_sentence_embedding_dimension()

# Global embedding service instance
embedding_service = EmbeddingService()