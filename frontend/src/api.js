import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000',
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    if (config.method === 'post' || config.method === 'patch') {
        config.headers['Idempotency-Key'] = crypto.randomUUID();
    }
    return config;
});

export default api;