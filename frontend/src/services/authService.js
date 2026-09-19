import apiClient from './apiClient';

const authService = {
  login: async (email, password, role) => {
    return await apiClient.post('/auth/login', { email, password, role });
  },
  getCurrentUser: async () => {
    return await apiClient.get('/auth/me');
  },
  signup: async (fullName, email, password, phone) => {
    return await apiClient.post('/auth/signup', { full_name: fullName, email, password, phone });
  },
  logout: async () => {
    return await apiClient.post('/auth/logout');
  }
};

export default authService;
