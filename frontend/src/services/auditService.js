import apiClient from './apiClient';

const auditService = {
  getAuditEvents: async (params = {}) => {
    return await apiClient.get('/audit/events', { params });
  },
  getAuditEventById: async (id) => {
    return await apiClient.get(`/audit/events/${id}`);
  },
  getAuditAnalytics: async () => {
    return await apiClient.get('/audit/analytics');
  }
};

export default auditService;
