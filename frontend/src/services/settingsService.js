import apiClient from './apiClient';

export const dashboardService = {
  getAdminDashboard: async () => apiClient.get('/dashboard/admin'),
  getOfficerDashboard: async () => apiClient.get('/dashboard/officer'),
  getReviewerDashboard: async () => apiClient.get('/dashboard/reviewer'),
  getAuditorDashboard: async () => apiClient.get('/dashboard/auditor'),
  getCitizenDashboard: async () => apiClient.get('/dashboard/citizen'),
};

export const settingsService = {
  getSettings: async () => apiClient.get('/settings'),
  updateSettings: async (settingsData) => apiClient.patch('/settings', settingsData),
};
