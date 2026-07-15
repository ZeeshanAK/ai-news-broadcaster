import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Articles
export const articlesAPI = {
  list: (params = {}) => client.get('/articles', { params }),
  get: (id) => client.get(`/articles/${id}`),
  create: (data) => client.post('/articles', data),
  update: (id, data) => client.patch(`/articles/${id}`, data),
  delete: (id) => client.delete(`/articles/${id}`),
}

// Sources
export const sourcesAPI = {
  list: (params = {}) => client.get('/sources', { params }),
  get: (id) => client.get(`/sources/${id}`),
  create: (data) => client.post('/sources', data),
  update: (id, data) => client.patch(`/sources/${id}`, data),
  delete: (id) => client.delete(`/sources/${id}`),
  fetch: (id) => client.post(`/sources/${id}/fetch`),
}

// Summaries
export const summariesAPI = {
  list: (params = {}) => client.get('/summaries', { params }),
  get: (id) => client.get(`/summaries/${id}`),
  create: (data) => client.post('/summaries', data),
  update: (id, data) => client.patch(`/summaries/${id}`, data),
  delete: (id) => client.delete(`/summaries/${id}`),
}

// Broadcasts
export const broadcastsAPI = {
  list: (params = {}) => client.get('/broadcasts', { params }),
  get: (id) => client.get(`/broadcasts/${id}`),
  create: (data) => client.post('/broadcasts', data),
  update: (id, data) => client.patch(`/broadcasts/${id}`, data),
  delete: (id) => client.delete(`/broadcasts/${id}`),
}

// Settings
export const settingsAPI = {
  list: (params = {}) => client.get('/settings', { params }),
  get: (key) => client.get(`/settings/${key}`),
  create: (data) => client.post('/settings', data),
  update: (key, data) => client.patch(`/settings/${key}`, data),
  delete: (key) => client.delete(`/settings/${key}`),
}

export default client