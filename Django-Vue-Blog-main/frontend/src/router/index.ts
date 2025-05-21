import { createRouter, createWebHistory } from 'vue-router'
import CategoryDetail from '@/views/CategoryDetail.vue'
import axios from 'axios'

// const ArticleDetail = () => import('@/views/ArticleDetail.vue')
// const UserCenter = () => import('@/views/UserCenter.vue')
// const ArticleCreate = () => import('@/views/ArticleCreate.vue')
// const ArticleEdit = () => import('@/views/ArticleEdit.vue')
const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/blog/Home.vue')
  },
  {
    path: '/now',
    name: 'Now',
    component: () => import('../views/blog/Now.vue')
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/blog/About.vue')
  },

  {
    path: '/essays',
    name: 'Essays',
    component: () => import('../views/blog/Essays.vue')
  },
  {
    path: '/notes',
    name: 'Notes',
    component: () => import('../views/blog/notes.vue')
  },
  {
    path: '/tech',
    name: 'Tech',
    component: () => import('../views/blog/tech.vue')
  },
  {
    path: '/books',
    name: 'Books',
    component: () => import('../views/blog/books.vue')
  },
  {
    path: '/manage',
    name: 'Manage',
    component: () => import('../views/manage/manageHome.vue')
  },

    {
    path: '/manage/article',
    name: 'ArticleManage',
    component: () => import('../views/manage/ArticleManage.vue')
  },
  {
    path: '/manage/category',
    name: 'TagManage',
    component: () => import('../views/manage/CategoryManage.vue')
  },
  {
    path: '/manage/comment',
    name: 'CommentManage',
    component: () => import('../views/manage/CommentManage.vue')
  },
  {
    path: '/manage/user',
    name: 'UserManage',
    component: () => import('../views/manage/UserManage.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue')
  },
  {
    path: '/tech/:id',
    name: 'TechDetail',
    component: () => import('../views/blog/article_detail.vue')
  },
  {
    path: '/essays/:id', 
    name: 'EssayDetail',
    component: () => import('../views/blog/article_detail.vue')
  },
  {
    path: '/notes/:id',
    name: 'NoteDetail', 
    component: () => import('../views/blog/article_detail.vue')
  },
  {
    path: '/garden/:id',
    name: 'GardenDetail',
    component: () => import('../views/blog/article_detail.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // 始终滚动到顶部
    return { top: 0 }
  }
})

// 检查用户是否是管理员
const checkIsAdmin = async () => {
  const token = localStorage.getItem('access_token')
  const username = localStorage.getItem('username')
  
  if (!token || !username) return false
  
  try {
    const response = await axios.get(`/api/user/${username}/`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    
    return response.data?.is_superuser === true
  } catch (error) {
    console.error('获取用户信息失败:', error)
    return false
  }
}

router.beforeEach(async (to, from, next) => {
  // 管理页面路由
  if (to.path.startsWith('/manage')) {
    const token = localStorage.getItem('access_token')
    
    // 未登录，跳转到登录页
    if (!token) {
      next('/login')
      return
    }
    
    // 检查是否是管理员
    const isAdmin = await checkIsAdmin()
    
    if (!isAdmin) {
      // 不是管理员，跳转到首页
      alert('只有管理员可以访问管理页面')
      next('/')
      return
    }
    
    // 是管理员，允许访问
    next()
  } else {
    // 非管理页面，正常访问
    next()
  }
})

export default router
