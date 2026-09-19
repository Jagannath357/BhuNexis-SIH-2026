import apiClient from './apiClient';

const documentService = {
  uploadDocument: async (formData) => {
    return await apiClient.post('/documents', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
  getDocuments: async (params = {}) => {
    return await apiClient.get('/documents', { params });
  },
  getDocumentById: async (documentId) => {
    return await apiClient.get(`/documents/${documentId}`);
  },
  getDocumentStatus: async (documentId) => {
    return await apiClient.get(`/documents/${documentId}/status`);
  }
};

export default documentService;
