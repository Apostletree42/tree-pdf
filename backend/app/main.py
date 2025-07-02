from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .core.config import settings
from .core.database import init_db
from .documents.router import router as documents_router
from .chat.router import router as chat_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting PDF Q&A Application...")
    init_db()
    print("✅ Database initialized")
    print(f"🔧 Environment: {settings.environment}")
    print(f"📁 Storage path: {settings.storage_path}")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down PDF Q&A Application...")


app = FastAPI(
    title="PDF Q&A Application",
    description="Upload PDFs and ask questions about their content",
    version="1.0.0",
    debug=settings.debug,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "PDF Q&A Application API",
        "status": "running",
        "environment": settings.environment
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "storage": "accessible"
    }

app.include_router(documents_router, prefix="/api/documents", tags=["documents"])
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.environment == "development" else False
    )