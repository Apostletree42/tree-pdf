import axios from 'axios';
import type { Document, UploadResponse, QuestionRequest, QuestionResponse } from '../types/index';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds for file uploads
});

export const documentsApi = {
  // Upload PDF document
  upload: async (file: File): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Get all documents
  getAll: async (): Promise<{ documents: Document[]; total: number }> => {
    const response = await api.get('/documents/');
    return response.data;
  },

  // Get single document
  getById: async (id: number): Promise<Document> => {
    const response = await api.get(`/documents/${id}`);
    return response.data;
  },

  // Delete document
  delete: async (id: number): Promise<{ message: string }> => {
    const response = await api.delete(`/documents/${id}`);
    return response.data;
  },
};

export const chatApi = {
  // Ask question
  ask: async (request: QuestionRequest): Promise<QuestionResponse> => {
    const response = await api.post('/chat/ask', request);
    return response.data;
  },

  // Get conversation history
  getHistory: async (documentId: number): Promise<{
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    conversations: any[];
    total: number;
    document_filename?: string;
  }> => {
    const response = await api.get(`/chat/history/${documentId}`);
    return response.data;
  },
};

export default api;