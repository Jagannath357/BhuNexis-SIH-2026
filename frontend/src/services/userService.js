import apiClient from './apiClient';

const userService = {
  getUsers: async (params = {}) => {
    return await apiClient.get('/users', { params });
  },
  getUserById: async (userId) => {
    return await apiClient.get(`/users/${userId}`);
  },
  createUser: async (userData) => {
    return await apiClient.post('/users', userData);
  },
  updateUser: async (userId, userData) => {
    return await apiClient.patch(`/users/${userId}`, userData);
  },
  updateUserStatus: async (userId, isActive) => {
    return await apiClient.patch(`/users/${userId}/status`, { is_active: isActive });
  },
  getProfile: async () => {
    return await apiClient.get('/profile');
  },
  updateProfile: async (data) => {
    return await apiClient.patch('/profile', data);
  },
  updatePassword: async (currentPassword, newPassword) => {
    return await apiClient.patch('/profile/password', {
      current_password: currentPassword,
      new_password: newPassword
    });
  }
};

export default userService;
