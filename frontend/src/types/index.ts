export interface Document {
  id: number;
  filename: string;
  original_filename: string;
  file_size: number;
  processed: boolean;
  processing_error?: string;
  chunk_count: number;
  upload_date: string;
  processed_date?: string;
  total_pages?: number;
  total_characters?: number;
}

export interface UploadResponse {
  document_id: number;
  message: string;
  filename: string;
  file_size: number;
  processing_started: boolean;
}

export interface Message {
  id: string;
  type: 'user' | 'ai';
  content: string;
  timestamp: Date;
  isLoading?: boolean;
}

export interface QuestionRequest {
  document_id: number;
  question: string;
}

export interface QuestionResponse {
  answer: string;
  question: string;
  document_id: number;
  context_chunks_used: number;
  response_time_seconds: number;
  conversation_id: number;
}

export interface ApiResponse<T> {
  data: T;
  error?: string;
}