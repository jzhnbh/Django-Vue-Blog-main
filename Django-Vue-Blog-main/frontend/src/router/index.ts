import { createRouter, createWebHistory } from 'vue-router'
import CategoryDetail from '@/views/CategoryDetail.vue'

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
    path: '/garden',
    name: 'Garden',
    component: () => import('../views/blog/Garden.vue')
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

// router.beforeEach((to, from, next) => {
//   if (to.path.startsWith('/manage')) {
//     const token = localStorage.getItem('access.myblog')
//     if (!token) {
//       next('/login')
//     } else {
//       next()
//     }
//   } else {
//     next()
//   }
// })

export default router
