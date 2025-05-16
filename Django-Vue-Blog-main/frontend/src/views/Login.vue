<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h2>欢迎回来</h2>
        <p>登录您的账户以继续</p>
      </div>
      
      <!-- 使用原生表单并添加novalidate防止浏览器验证 -->
      <form @submit.prevent="submitForm" novalidate autocomplete="off">
        <el-form 
          ref="loginForm" 
          :model="loginData" 
          :rules="rules" 
          label-position="top"
          class="login-form"
        >
          <el-form-item label="用户名" prop="username">
            <el-input 
              v-model="loginData.username" 
              placeholder="请输入用户名"
              prefix-icon="User"
              name="username"
              autocomplete="username"
            />
          </el-form-item>
          
          <el-form-item label="密码" prop="password">
            <el-input 
              v-model="loginData.password" 
              type="password" 
              placeholder="请输入密码"
              prefix-icon="Lock"
              show-password
              @keyup.enter.prevent="submitForm"
              name="current-password"
              autocomplete="off"
            />
          </el-form-item>
          
          <div class="remember-me">
            <el-checkbox v-model="rememberMe">记住我</el-checkbox>
            <el-link type="primary" :underline="false">忘记密码?</el-link>
          </div>
          
          <el-button 
            type="primary" 
            :loading="loading" 
            @click.prevent="submitForm"
            class="login-button"
            native-type="submit"
          >
            登录
          </el-button>
          
          <div class="register-link">
            <span>还没有账户?</span>
            <el-link type="primary" :underline="false" @click.prevent="goToRegister">立即注册</el-link>
          </div>
        </el-form>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, FormInstance, FormRules } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import api from '../api'

const router = useRouter()
const loading = ref(false)
const rememberMe = ref(false)

// 表单数据
const loginData = reactive({
  username: '',
  password: ''
})

// 表单引用
const loginForm = ref<FormInstance>()

const rules = reactive<FormRules>({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应在3-20个字符之间', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少为6个字符', trigger: 'blur' }
  ]
})

// 登录成功后的处理
const handleLoginSuccess = (accessToken: string, refreshToken: string, username: string) => {
  // 保存token到本地存储
  localStorage.setItem('access_token', accessToken)
  localStorage.setItem('refresh_token', refreshToken)
  localStorage.setItem('username', username)
  
  // 清除会话存储中的重定向标记
  sessionStorage.removeItem('auth_redirected')
  
  // 提示成功
  ElMessage.success('登录成功')
  
  // 检查是否有登录后需要重定向的页面
  const redirectPath = sessionStorage.getItem('redirect_after_login')
  if (redirectPath) {
    sessionStorage.removeItem('redirect_after_login') // 清除重定向记录
    router.push(redirectPath)
  } else {
    // 否则导航到首页
    router.push('/')
  }
}

// 前往注册页面
const goToRegister = () => {
  router.push('/register')
}

const submitForm = async (e?: Event) => {
  // 阻止表单默认提交行为，这是导致闪烁和触发密码管理器的原因
  if (e) e.preventDefault();
  
  if (!loginForm.value) return
  
  try {
    // 验证表单
    const valid = await loginForm.value.validate()
    if (!valid) return
    
    // 设置加载状态
    loading.value = true
    
    // 打印登录请求信息（开发调试用）
    console.log('发送登录请求:', {
      username: loginData.username,
      password: loginData.password?.length ? `长度为${loginData.password.length}` : '空密码' // 不打印实际密码
    })
    
    // 确保登录请求格式正确
    const loginFormData = {
      username: loginData.username.trim(),  // 移除空格
      password: loginData.password
    }
    
    // 发送登录请求
    const response = await api.post('/token/', loginFormData)
    
    // 打印登录响应（开发调试用）
    console.log('登录成功:', {
      access: response.data.access ? '已获取token' : '未获取token',
      refresh: response.data.refresh ? '已获取刷新token' : '未获取刷新token'
    })
    
    // 处理登录成功
    handleLoginSuccess(
      response.data.access,
      response.data.refresh,
      loginData.username
    )
  } catch (error: any) {
    console.error('登录失败:', error)
    
    // 打印详细错误信息
    if (error.response) {
      console.error('错误状态码:', error.response.status)
      console.error('错误响应数据:', error.response.data)
      
      // 根据不同错误显示不同提示
      if (error.response.data.detail) {
        // 在用户界面显示Django返回的详细错误消息
        ElMessage({
          message: `登录失败: ${error.response.data.detail}`,
          type: 'error',
          duration: 5000,
          showClose: true
        })
        
        // 如果是用户不存在或密码错误，给出更具体的建议
        if (error.response.data.detail.includes('有效用户')) {
          ElMessage({
            message: '此用户名可能不存在，请检查拼写或注册新账号',
            type: 'warning',
            duration: 5000,
            showClose: true
          })
        }
      } else {
        ElMessage({
          message: '用户名或密码错误，请重试',
          type: 'error',
          duration: 4000,
          showClose: true
        })
      }
    } else {
      // 显示错误消息，但不清空表单和不导致页面闪烁
      ElMessage({
        message: '登录失败，请检查网络连接',
        type: 'error',
        duration: 4000,
        showClose: true
      })
    }
  } finally {
    loading.value = false
  }
}

// 如果是从cookie或localStorage恢复的会话，可以在这里处理
onMounted(() => {
  // 检查是否已经登录
  const token = localStorage.getItem('access_token')
  if (token) {
    // 已登录用户直接跳转首页
    // 如果需要的话，取消下面这行的注释
    // router.push('/')
  }
  
  // 从localStorage恢复存储的用户名(如果勾选了记住我)
  if (localStorage.getItem('remember_username')) {
    loginData.username = localStorage.getItem('remember_username') || ''
    rememberMe.value = true
  }
})
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
  box-sizing: border-box;
  padding: 0 20px;
}

.login-card {
  width: 100%;
  max-width: 420px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
  padding: 40px;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h2 {
  font-size: 24px;
  color: #303133;
  margin-bottom: 8px;
  font-weight: 500;
}

.login-header p {
  color: #909399;
  font-size: 14px;
}

.login-form {
  margin-top: 20px;
}

.remember-me {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.login-button {
  width: 100%;
  padding: 12px 0;
  font-size: 16px;
  margin-bottom: 16px;
}

.register-link {
  text-align: center;
  color: #606266;
  font-size: 14px;
  margin-top: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

:deep(.el-input__wrapper) {
  padding: 8px 12px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}
</style> 