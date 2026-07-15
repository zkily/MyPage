import axios from 'axios'
import type { LangCode } from '@/types'

const api = axios.create({
  baseURL: '/api',
  timeout: 15000,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('admin_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export function setAuthToken(token: string | null) {
  if (token) {
    localStorage.setItem('admin_token', token)
  } else {
    localStorage.removeItem('admin_token')
  }
}

export function getAuthToken(): string | null {
  return localStorage.getItem('admin_token')
}

export const publicApi = {
  getProjects: (lang: LangCode) => api.get('/projects', { params: { lang } }),
  getProject: (slug: string, lang: LangCode) => api.get(`/projects/${slug}`, { params: { lang } }),
  getKnowledge: (lang: LangCode) => api.get('/knowledge', { params: { lang } }),
  getKnowledgeArticle: (slug: string, lang: LangCode) =>
    api.get(`/knowledge/${slug}`, { params: { lang } }),
}

export const adminApi = {
  login: (username: string, password: string) =>
    api.post('/auth/login', { username, password }),
  getStats: () => api.get('/admin/stats'),
  upload: (file: File) => {
    const form = new FormData()
    form.append('file', file)
    return api.post('/admin/upload', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  listProjects: () => api.get('/admin/projects'),
  getProject: (id: number) => api.get(`/admin/projects/${id}`),
  createProject: (data: Record<string, unknown>) => api.post('/admin/projects', data),
  updateProject: (id: number, data: Record<string, unknown>) =>
    api.put(`/admin/projects/${id}`, data),
  deleteProject: (id: number) => api.delete(`/admin/projects/${id}`),
  listKnowledge: () => api.get('/admin/knowledge'),
  getKnowledge: (id: number) => api.get(`/admin/knowledge/${id}`),
  createKnowledge: (data: Record<string, unknown>) => api.post('/admin/knowledge', data),
  updateKnowledge: (id: number, data: Record<string, unknown>) =>
    api.put(`/admin/knowledge/${id}`, data),
  deleteKnowledge: (id: number) => api.delete(`/admin/knowledge/${id}`),
}

export default api
