import React, { useState, useEffect } from 'react';
import type { Document, Message } from './types';
import { documentsApi } from './services/api';
import { generateId } from './utils/helpers';
import './App.css';
import Header from './components/Header';
import ChatInterface from './components/ChatInterface';
import DocumentSelector from './components/DocumentSelector';

function App() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [selectedDocument, setSelectedDocument] = useState<Document | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  // Load documents on mount
  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      const response = await documentsApi.getAll();
      setDocuments(response.documents);
      
      // Auto-select first processed document
      const processedDoc = response.documents.find(doc => doc.processed);
      if (processedDoc && !selectedDocument) {
        setSelectedDocument(processedDoc);
      }
    } catch (error) {
      console.error('Error loading documents:', error);
    }
  };

  const handleDocumentUpload = async (file: File) => {
    setIsLoading(true);
    try {
      const uploadResponse = await documentsApi.upload(file);
      await loadDocuments(); // Refresh document list
      
      // Find and select the uploaded document
      const newDoc = documents.find(doc => doc.id === uploadResponse.document_id);
      if (newDoc?.processed) {
        setSelectedDocument(newDoc);
        setMessages([]); // Clear chat for new document
      }
    } catch (error) {
      console.error('Error uploading document:', error);
      alert('Error uploading document. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDocumentSelect = (document: Document) => {
    setSelectedDocument(document);
    setMessages([]); // Clear chat when switching documents
  };

  const addMessage = (message: Omit<Message, 'id' | 'timestamp'>) => {
    const newMessage: Message = {
      ...message,
      id: generateId(),
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, newMessage]);
    return newMessage.id;
  };

  const updateMessage = (id: string, updates: Partial<Message>) => {
    setMessages(prev => prev.map(msg => 
      msg.id === id ? { ...msg, ...updates } : msg
    ));
  };

  return (
    <div className="app">
      <Header />
      <div className="app-content">
        <DocumentSelector
          documents={documents}
          selectedDocument={selectedDocument}
          onDocumentSelect={handleDocumentSelect}
          onDocumentUpload={handleDocumentUpload}
          isLoading={isLoading}
        />
        <ChatInterface
          selectedDocument={selectedDocument}
          messages={messages}
          onAddMessage={addMessage}
          onUpdateMessage={updateMessage}
        />
      </div>
    </div>
  );
}

export default App;