<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <h2>创建账户</h2>
        <p>注册一个新账户以开始使用</p>
      </div>
      
      <el-form 
        ref="registerForm" 
        :model="registerData" 
        :rules="rules" 
        label-position="top"
        class="register-form"
      >
        <el-form-item label="用户名" prop="username">
          <el-input 
            v-model="registerData.username" 
            placeholder="请输入用户名"
            prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input 
            v-model="registerData.email" 
            placeholder="请输入邮箱"
            prefix-icon="Message"
          />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input 
            v-model="registerData.password" 
            type="password" 
            placeholder="请输入密码"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input 
            v-model="registerData.confirmPassword" 
            type="password" 
            placeholder="请再次输入密码"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <el-button 
          type="primary" 
          :loading="loading" 
          @click="submitForm"
          class="register-button"
        >
          注册
        </el-button>
        
        <div class="login-link">
          <span>已有账户?</span>
          <el-link type="primary" :underline="false" @click="router.push('/login')">立即登录</el-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, FormInstance, FormRules } from 'element-plus'
import { User, Lock, Message } from '@element-plus/icons-vue'
import api from '../api'

const router = useRouter()
const loading = ref(false)

// 表单数据
const registerData = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

// 表单引用
const registerForm = ref<FormInstance>()

// 验证密码是否一致
const validatePass = (rule: any, value: string, callback: any) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== registerData.password) {
    callback(new Error('两次输入密码不一致!'))
  } else {
    callback()
  }
}

// 验证邮箱格式
const validateEmail = (rule: any, value: string, callback: any) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (value === '') {
    callback(new Error('请输入邮箱'))
  } else if (!emailRegex.test(value)) {
    callback(new Error('请输入有效的邮箱地址'))
  } else {
    callback()
  }
}

const rules = reactive<FormRules>({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应在3-20个字符之间', trigger: 'blur' }
  ],
  email: [
    { required: true, validator: validateEmail, trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少为6个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validatePass, trigger: 'blur' }
  ]
})

const submitForm = async () => {
  if (!registerForm.value) return
  
  await registerForm.value.validate(async (valid) => {
    if (!valid) return
    
    loading.value = true
    
    try {
      await api.post('/user/', {
        username: registerData.username,
        email: registerData.email,
        password: registerData.password
      })
      
      ElMessage.success('注册成功！请登录')
      router.push('/login')
    } catch (error: any) {
      console.error('注册失败:', error)
      if (error.response?.data) {
        const errors = error.response.data
        if (errors.username) {
          ElMessage.error(errors.username[0])
        } else if (errors.email) {
          ElMessage.error(errors.email[0])
        } else {
          ElMessage.error('注册失败，请稍后重试')
        }
      } else {
        ElMessage.error('注册失败，请稍后重试')
      }
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
  box-sizing: border-box;
  padding: 10px 20px;
}

.register-card {
  width: 100%;
  max-width: 420px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
  padding: 25px;
}

.register-header {
  text-align: center;
  margin-bottom: 15px;
}

.register-header h2 {
  font-size: 22px;
  color: #303133;
  margin-bottom: 5px;
  font-weight: 500;
}

.register-header p {
  color: #909399;
  font-size: 14px;
}

.register-form {
  margin-top: 15px;
}

:deep(.el-form-item) {
  margin-bottom: 15px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  padding-bottom: 5px;
  line-height: 1.2;
}

:deep(.el-input__wrapper) {
  padding: 5px 10px;
}

.register-button {
  width: 100%;
  padding: 10px 0;
  font-size: 16px;
  margin-top: 5px;
  margin-bottom: 12px;
}

.login-link {
  text-align: center;
  color: #606266;
  font-size: 14px;
  margin-top: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
</style> 