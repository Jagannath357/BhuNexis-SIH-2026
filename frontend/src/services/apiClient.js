import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request Interceptor: Attach JWT Bearer Token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('bhunexis_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response Interceptor: Format error responses & handle 401
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response) {
      const errData = error.response.data;
      if (error.response.status === 401) {
        // Clear token on 401 unauthorized
        localStorage.removeItem('bhunexis_token');
      }
      return Promise.reject(errData?.error || { code: 'API_ERROR', message: 'An unexpected API error occurred.' });
    }
    return Promise.reject({ code: 'NETWORK_ERROR', message: 'Unable to connect to BhuNexis backend server.' });
  }
);

export default apiClient;
