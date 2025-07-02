from typing import List
import re

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split text into overlapping chunks
    Args:
        text: Input text to chunk
        chunk_size: Maximum characters per chunk
        overlap: Number of characters to overlap between chunks
    Returns: List of text chunks
    """
    if not text or not text.strip():
        return []
    text = clean_text(text)

    if len(text) <= chunk_size:
        return [text]
        
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # If this is not the last chunk, try to break at sentence or word boundary
        if end < len(text):
            # break at sentence end
            sentence_break = text.rfind('.', start, end)
            if sentence_break > start:
                end = sentence_break + 1
            else:
                # break at word boundary
                word_break = text.rfind(' ', start, end)
                if word_break > start:
                    end = word_break
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = max(start + 1, end - overlap)
        if start >= len(text):
            break
    
    return chunks

def clean_text(text: str) -> str:
    """
    Clean and normalize text
    Args:
        text: Input text to clean
    Returns: Cleaned text
    """
    if not text:
        return ""
    
    # whitespaces removed
    text = re.sub(r'\s+', ' ', text)
    
    # special characters removed
    text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', '', text)
    
    # consecutive punctuations removed
    text = re.sub(r'[\.]{2,}', '.', text)
    text = re.sub(r'[,]{2,}', ',', text)
    
    # Strip and return
    return text.strip()

def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """
    Extract important keywords from text (simple implementation)
    Args:
        text: Input text
        max_keywords: Maximum number of keywords to return
    Returns: List of keywords
    """
    if not text:
        return []
    
    # Simple keyword extraction based on word frequency
    # Remove common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
        'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
        'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
        'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
    }
    
    # Extract words
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Filter out stop words and short words
    keywords = [word for word in words if len(word) > 3 and word not in stop_words]
    word_freq = {}
    for word in keywords:
        word_freq[word] = word_freq.get(word, 0) + 1
    sorted_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    
    return [word for word, freq in sorted_keywords[:max_keywords]]