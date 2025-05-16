import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // 检查是否为POST或PUT请求并且有请求体
    if ((config.method === 'post' || config.method === 'put') && config.data) {
      // 记录请求日志，便于调试
      console.log('API请求:', config.url, config.data)
    }
    
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response
  },
  error => {
    if (error.response?.status === 401) {
      // 只有当访问需要登录的API时，才清除token并重定向
      // 检查当前页面是否已经在登录页，避免循环重定向
      const isLoginPage = window.location.pathname === '/login'
      
      if (!isLoginPage) {
        // 避免反复清除token和重定向
        const hasRedirected = sessionStorage.getItem('auth_redirected')
        
        if (!hasRedirected) {
          // 标记已经重定向过，防止多次跳转
          sessionStorage.setItem('auth_redirected', 'true')
          
          // 清除身份验证Token
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          
          // 保存当前路径，以便登录后可以返回
          sessionStorage.setItem('redirect_after_login', window.location.pathname)
          
          // 可以使用更友好的方式提示用户，比如弹窗
          console.error('您的登录状态已过期或无效，即将跳转到登录页面')
          
          // 延迟一下，给用户时间看到错误信息
          setTimeout(() => {
            window.location.href = '/login'
          }, 1000)
        }
      }
    }
    
    return Promise.reject(error)
  }
)

export default api 