<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h2>欢迎回来</h2>
        <p>登录您的账户以继续</p>
      </div>
      
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
          />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input 
            v-model="loginData.password" 
            type="password" 
            placeholder="请输入密码"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <div class="remember-me">
          <el-checkbox v-model="rememberMe">记住我</el-checkbox>
          <el-link type="primary" :underline="false">忘记密码?</el-link>
        </div>
        
        <el-button 
          type="primary" 
          :loading="loading" 
          @click="submitForm"
          class="login-button"
        >
          登录
        </el-button>
        
        <div class="register-link">
          还没有账户? <el-link type="primary" :underline="false">立即注册</el-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, FormInstance, FormRules } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import api from '@/api'

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

const submitForm = async () => {
  if (!loginForm.value) return
  
  await loginForm.value.validate(async (valid) => {
    if (!valid) return
    
    loading.value = true
    
    try {
      const response = await api.post('/token/', {
        username: loginData.username,
        password: loginData.password
      })
      
      // 保存token
      localStorage.setItem('access_token', response.data.access)
      localStorage.setItem('refresh_token', response.data.refresh)
      router.push('/')
      ElMessage.success('登录成功')

    } catch (error) {
      console.error('登录失败:', error)
      ElMessage.error('用户名或密码错误')
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 20px;
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
}

:deep(.el-input__wrapper) {
  padding: 8px 12px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}
</style> 