<template>
  <nav class="top-nav">
    <div class="logo" @click="router.push('/')">
      <span class="m-left">◀</span>
      <span class="m">JZH</span>
      <span class="m-right">▶</span>
    </div>
    <div class="nav-links">
      <router-link to="/garden">花园</router-link>
      <router-link to="/now">现在</router-link>
      <router-link to="/about">关于</router-link>
      <router-link v-if="isAdmin" to="/manage">管理</router-link>
      <router-link v-if="!isLoggedIn" to="/login">登录</router-link>
      <a v-else href="#" @click.prevent="handleLogout">退出</a>
    </div>
  </nav>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '../api'

export default {
  name: 'Top',
  setup() {
    const router = useRouter()
    const userInfo = ref(null)

    // 检查用户是否已登录
    const isLoggedIn = computed(() => {
      return !!localStorage.getItem('access_token')
    })

    // 检查用户是否是管理员
    const isAdmin = computed(() => {
      return userInfo.value?.is_superuser === true
    })

    // 加载用户信息
    const loadUserInfo = async () => {
      if (!isLoggedIn.value) return
      
      try {
        // 获取当前登录用户名
        const username = localStorage.getItem('username')
        if (!username) return
        
        // 获取用户详细信息
        const response = await api.get(`/user/${username}/`)
        userInfo.value = response.data
      } catch (error) {
        console.error('获取用户信息失败:', error)
      }
    }

    // 退出登录
    const handleLogout = () => {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('username')
      userInfo.value = null
      ElMessage.success('退出成功')
      router.push('/login')
    }

    onMounted(() => {
      loadUserInfo()
    })

    return {
      router,
      isLoggedIn,
      isAdmin,
      handleLogout
    }
  }
}
</script>

<style scoped>
.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4rem;
  padding: 0 20px;  /* 添加内边距 */
  box-sizing: border-box;
  max-width: 100%;  /* 确保不超出视口 */
}

.logo {
  display: flex;
  align-items: center;
  font-size: 1.5rem;
  font-weight: bold;
  cursor: pointer;
}

.m-left, .m-right {
  color: #00a0e9;
}

.m {
  margin: 0 0.25rem;
}

.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-links a {
  text-decoration: none;
  color: #333;
  font-size: 1rem;
}

.nav-links a:hover {
  color: #00a0e9;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .nav-links {
    gap: 1rem;
  }
  
  .logo {
    font-size: 1.2rem;
  }
}
</style>