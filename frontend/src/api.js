import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'https://digital-banking-wgqs.onrender.com',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  if (config.method === 'post' || config.method === 'patch') {
    // Only inject Idempotency-Key if not logging in or registering
    if (!config.url.includes('/login') && !config.url.includes('/register')) {
      config.headers['Idempotency-Key'] = crypto.randomUUID();
    }
  }
  return config;
});

export default api;