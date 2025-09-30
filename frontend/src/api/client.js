import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8001';
export const API = `${API_BASE}/api`;

// Create axios instance
const apiClient = axios.create({
  baseURL: API,
});

// Add token to requests if available
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// API functions
export const catalogApi = {
  getItems: (params) => apiClient.get('/catalog', { params }),
  getItem: (id) => apiClient.get(`/catalog/${id}`),
};

export const ordersApi = {
  create: (data) => apiClient.post('/orders', data),
  getAll: (params) => apiClient.get('/orders', { params }),
  getById: (id) => apiClient.get(`/orders/${id}`),
  updateStatus: (id, data) => apiClient.patch(`/orders/${id}/status`, data),
};

export const inventoryApi = {
  getAll: (params) => apiClient.get('/inventory', { params }),
  getById: (id) => apiClient.get(`/inventory/${id}`),
  create: (data) => apiClient.post('/inventory', data),
  update: (id, data) => apiClient.patch(`/inventory/${id}`, data),
  delete: (id) => apiClient.delete(`/inventory/${id}`),
};

export const authApi = {
  login: (data) => apiClient.post('/auth/login', data),
  register: (data) => apiClient.post('/auth/register', data),
  getMe: () => apiClient.get('/auth/me'),
};

export default apiClient;