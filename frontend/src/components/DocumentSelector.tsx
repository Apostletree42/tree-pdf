import React, { useRef } from 'react';
import { Plus, FileText } from 'lucide-react';
import type { Document } from '../types/index';
import { isValidPDF } from '../utils/helpers';

interface DocumentSelectorProps {
    documents: Document[];
    selectedDocument: Document | null;
    onDocumentSelect: (document: Document) => void;
    onDocumentUpload: (file: File) => void;
    isLoading: boolean;
}

function DocumentSelector({
    documents,
    selectedDocument,
    onDocumentSelect,
    onDocumentUpload,
    isLoading,
}: DocumentSelectorProps) {
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            if (!isValidPDF(file)) {
                alert('Please select a PDF file.');
                return;
            }
            onDocumentUpload(file);
        }
        // Reset input
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    };

    const handleUploadClick = () => {
        fileInputRef.current?.click();
    };

    const processedDocuments = documents.filter(doc => doc.processed);

    return (
        <div className="document-selector">
            <div className="document-selector-content">
                {/* Current Document */}
                {selectedDocument ? (
                    <div className="current-document">
                        <FileText className="document-icon" />
                        <span className="document-name">
                            {selectedDocument.original_filename.replace('.pdf', '')}
                        </span>
                    </div>
                ) : (
                    <div className="no-document">
                        <span>No document selected</span>
                    </div>
                )}

                {/* Upload button */}
                <button
                    className="upload-button"
                    onClick={handleUploadClick}
                    disabled={isLoading}
                >
                    <Plus className="plus-icon" />
                    {isLoading && <div className="spinner"></div>}
                </button>

                {/* Hidden file input */}
                <input
                    ref={fileInputRef}
                    type="file"
                    accept=".pdf,application/pdf"
                    onChange={handleFileSelect}
                    style={{ display: 'none' }}
                />
            </div>

            {/* Document List for multiple documents */}
            {processedDocuments.length > 1 && (
                <div className="document-list">
                    {processedDocuments.map(doc => (
                        <div
                            key={doc.id}
                            className={`document-item ${selectedDocument?.id === doc.id ? 'selected' : ''}`}
                            onClick={() => onDocumentSelect(doc)}
                        >
                            <FileText className="document-icon-small" />
                            <span className="document-name-small">
                                {doc.original_filename.replace('.pdf', '')}
                            </span>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default DocumentSelector;