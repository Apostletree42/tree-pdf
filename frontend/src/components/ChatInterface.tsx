import React, { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';
import MessageBubble from './MessageBubble';
import type { Document, Message } from '../types';
import { chatApi } from '../services/api';

interface ChatInterfaceProps {
    selectedDocument: Document | null;
    messages: Message[];
    onAddMessage: (message: Omit<Message, 'id' | 'timestamp'>) => string;
    onUpdateMessage: (id: string, updates: Partial<Message>) => void;
}

function ChatInterface({
    selectedDocument,
    messages,
    onAddMessage,
    onUpdateMessage,
}: ChatInterfaceProps) {
    const [question, setQuestion] = useState('');
    const [isAsking, setIsAsking] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Auto scroll to bottom
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!question.trim() || !selectedDocument || isAsking) return;
        const userQuestion = question.trim();
        setQuestion('');
        setIsAsking(true);

        try {
            // Add user message
            onAddMessage({
                type: 'user',
                content: userQuestion,
            });
            // Add loading message for AI response
            const loadingMessageId = onAddMessage({
                type: 'ai',
                content: 'Thinking...',
                isLoading: true,
            });
            const response = await chatApi.ask({
                document_id: selectedDocument.id,
                question: userQuestion,
            });

            // Update AI message with response
            onUpdateMessage(loadingMessageId, {
                content: response.answer,
                isLoading: false,
            });

        } catch (error) {
            console.error('Error asking question:', error);
            const loadingMessage = messages.find(m => m.isLoading);
            if (loadingMessage) {
                onUpdateMessage(loadingMessage.id, {
                    content: 'Sorry, I encountered an error processing your question. Please try again.',
                    isLoading: false,
                });
            }
        } finally {
            setIsAsking(false);
        }
    };

    if (!selectedDocument) {
        return (
            <div className="chat-interface">
                <div className="no-document-message">
                    <h3>Welcome to PDF Q&A</h3>
                    <p>Upload a PDF document to start asking questions about its content.</p>
                </div>
            </div>
        );
    }

    if (!selectedDocument.processed) {
        return (
            <div className="chat-interface">
                <div className="processing-message">
                    <h3>Processing Document...</h3>
                    <p>Please wait while we process your PDF. This usually takes a few moments.</p>
                    <div className="spinner"></div>
                </div>
            </div>
        );
    }

    return (
        <div className="chat-interface">
            {/* Messages */}
            <div className="messages-container">
                {messages.length === 0 ? (
                    <div className="welcome-message">
                        <h3>Ask me anything about your document!</h3>
                        <p>I've processed "{selectedDocument.original_filename}" and I'm ready to answer your questions.</p>
                    </div>
                ) : (
                    messages.map(message => (
                        <MessageBubble key={message.id} message={message} />
                    ))
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input box */}
            <form className="message-form" onSubmit={handleSubmit}>
                <div className="input-container">
                    <textarea
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter' && !e.shiftKey) {
                                e.preventDefault();
                                handleSubmit(e);
                            }
                        }}
                        placeholder="Send a message... (Shift+Enter for new line)"
                        disabled={isAsking}
                        className="message-input"
                        rows={1}
                        style={{
                            minHeight: '40px',
                            maxHeight: '120px',
                            resize: 'none',
                            overflow: 'auto'
                        }}
                    />
                    <button
                        type="submit"
                        disabled={!question.trim() || isAsking}
                        className="send-button"
                    >
                        <Send className="send-icon" />
                    </button>
                </div>
            </form>
        </div>
    );
}

export default ChatInterface;