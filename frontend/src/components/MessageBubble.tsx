import React from 'react';
import ReactMarkdown from 'react-markdown';
import type { Message } from '../types';

interface MessageBubbleProps {
    message: Message;
}

function MessageBubble({ message }: MessageBubbleProps) {
    return (
        <div className={`message-bubble ${message.type}`}>
            <div className="message-avatar">
                {message.type === 'user' ? (
                    <div className="user-avatar">S</div>
                ) : (
                    <div className="ai-avatar">ai</div>
                )}
            </div>
            <div className="message-content">
                <div className="message-text">
                    {message.isLoading ? (
                        <div className="typing-indicator">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    ) : message.type === 'ai' ? (
                        <ReactMarkdown>{message.content}</ReactMarkdown>
                    ) : (
                        message.content
                    )}
                </div>
                <div className="message-time">
                    {message.timestamp.toLocaleTimeString([], { 
                        hour: '2-digit', 
                        minute: '2-digit' 
                    })}
                </div>
            </div>
        </div>
    );
}

export default MessageBubble;