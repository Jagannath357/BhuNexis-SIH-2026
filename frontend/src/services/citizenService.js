import apiClient from './apiClient';

const citizenService = {
  getMyRecords: async () => {
    return await apiClient.get('/citizen/my-records');
  },
  searchVerifiedRecords: async (params = {}) => {
    return await apiClient.get('/citizen/search', { params });
  },
  getRecordDetail: async (id) => {
    return await apiClient.get(`/citizen/records/${id}`);
  },
  downloadCertifiedRecord: async (id) => {
    return await apiClient.get(`/citizen/records/${id}/download`);
  },
  submitGrievance: async (grievanceData) => {
    return await apiClient.post('/citizen/grievances', grievanceData);
  }
};

export default citizenService;
