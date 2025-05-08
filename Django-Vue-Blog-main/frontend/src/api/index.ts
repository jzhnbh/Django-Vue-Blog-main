import axios from 'axios'
import store from '@/store'
import router from '../router'

const api = axios.create({
  baseURL: '/api'
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    const token = store.state.token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }else{ router.push('/login')}
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      // token 过期，尝试使用 refresh token
      const refreshToken = store.state.refreshToken
      if (refreshToken) {
        try {
          const response = await axios.post('/api/token/refresh/', {
            refresh: refreshToken
          })
          const newToken = response.data.access
          store.commit('setToken', newToken)
          localStorage.setItem('access_token', newToken)
          
          // 重试原请求
          error.config.headers.Authorization = `Bearer ${newToken}`
          return api.request(error.config)
        } catch (refreshError) {
          // refresh token 也过期了，需要重新登录
          store.dispatch('logout')
          window.location.href = '/login'
        }
      }
    }
    return Promise.reject(error)
  }
)

export default api 