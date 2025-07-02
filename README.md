# tree-pdf

# PDF Q&A Application

A full-stack RAG (Retrieval Augmented Generation) application that allows users to upload PDF documents and ask intelligent questions about their content using AI.

## 🚀 Features

- **PDF Upload & Processing**: Upload PDF documents with automatic text extraction
- **Intelligent Q&A**: Ask questions and get AI-powered answers based on document content
- **Vector Search**: Uses FAISS for semantic similarity search
- **Multi-Document Support**: Handle multiple PDFs simultaneously
- **Real-time Chat Interface**: Clean, responsive chat UI
- **Conversation History**: Track questions and answers per document

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL/SQLite** - Document metadata storage
- **Google Gemini** - Large Language Model for question answering
- **FAISS** - Vector similarity search
- **LangChain** - LLM orchestration framework
- **PyMuPDF** - PDF text extraction
- **Sentence Transformers** - Text embeddings

### Frontend
- **React** with **TypeScript** - Modern web UI
- **Axios** - HTTP client for API communication
- **React Markdown** - Markdown rendering for AI responses
- **Lucide React** - Icon library
- **Custom CSS** - Responsive design

## 📁 Project Structure

```
tree-pdf/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── core/              # Configuration and database
│   │   ├── documents/         # PDF upload and processing
│   │   ├── chat/              # Q&A functionality
│   │   ├── rag/               # RAG engine (embeddings, vector store)
│   │   └── main.py            # FastAPI application
│   ├── storage/               # File and index storage
│   │   ├── uploads/           # Uploaded PDF files
│   │   └── indexes/           # FAISS vector indexes
│   └── requirements.txt
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── services/          # API client
│   │   ├── types/             # TypeScript interfaces
│   │   └── utils/             # Helper functions
│   └── package.json
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Google Gemini API key

### Backend Setup

1. **Clone and navigate to backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment configuration**
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

4. **Start backend server**
   ```bash
   cd app
   python main.py
   ```
   Backend runs on: `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server**
   ```bash
   npm start
   ```
   Frontend runs on: `http://localhost:5173`

## 📖 API Documentation

### Document Endpoints

#### Upload PDF
```http
POST /api/documents/upload
Content-Type: multipart/form-data

Body: file (PDF)
```

#### List Documents
```http
GET /api/documents/
```

#### Get Document
```http
GET /api/documents/{document_id}
```

### Chat Endpoints

#### Ask Question
```http
POST /api/chat/ask
Content-Type: application/json

{
  "document_id": 1,
  "question": "What is this document about?"
}
```

#### Get Conversation History
```http
GET /api/chat/history/{document_id}
```

## 🏗️ Architecture Overview

### RAG Pipeline
1. **Document Processing**: PDF → Text extraction → Text chunking
2. **Indexing**: Text chunks → Embeddings → FAISS vector store
3. **Query Processing**: Question → Embedding → Similarity search
4. **Answer Generation**: Retrieved context + Question → Gemini → Answer

### Data Flow
```
User uploads PDF → Backend processes → Store in DB + Vector index
User asks question → Search vectors → Retrieve context → Generate answer
```

## 🔧 Configuration

### Environment Variables
```env
# Required
GEMINI_API_KEY=your_gemini_api_key

# Optional
DATABASE_URL=sqlite:///./storage/app.db
UPLOAD_MAX_SIZE=10485760
STORAGE_PATH=./storage
ENVIRONMENT=development
```

## 🎯 Usage

1. **Start both backend and frontend servers**
2. **Open browser to frontend URL**
3. **Upload a PDF document** using the + button
4. **Wait for processing** (usually 10-30 seconds)
5. **Ask questions** about the document content
6. **Get AI-powered answers** based on the document

## 📊 Performance

- **Processing Speed**: ~2-5 seconds per page
- **Response Time**: ~3-5 seconds per question
- **Supported File Size**: Up to 10MB PDFs
- **Accuracy**: High context-aware and grounded responses using semantic search

## 🔮 Future Enhancements

- Document metadata extraction (title, summary, type)
- Multi-language support
- OCR for image-based PDFs
- Advanced conversation memory
- Cloud storage integration (AWS S3)
- User authentication and document sharing

## 🐛 Troubleshooting

### Common Issues

**"Document not processing"**
- Check PDF is text-based (not scanned images)
- Verify Gemini API key is valid
- Check backend logs for errors

**"Vector index not found"**
- Ensure document processing completed successfully
- Check `storage/indexes/` directory exists

## 📄 License

This project is for educational purposes as part of a fullstack internship assignment.


---

## 🚀 Demo

[Live Demo Link] | [Demo Video Link]