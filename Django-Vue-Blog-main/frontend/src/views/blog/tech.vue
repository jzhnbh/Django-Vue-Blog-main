<template>
    <div class="notes">
      <Top />
      <div class="min-h">
      <!-- Header Section -->
      <div class="max-w-7xl">
        <h1 class="tex">技术</h1>
        <p class="text-xl text-gray-600">从我自己的观察和研究中收集的设计模式目录。</p>
      </div>
  
      <!-- Article Grid Container -->
      <div class="blog-container">
    <div class="post-grid">
      <article 
        v-for="article in articles" 
        :key="article.id" 
        class="post-item"
        @click="goToDetail(article.id)"
      >
        <div class="post-header">
          <div class="post-icon">◇</div>
          <div class="post-content">
            <h2 class="post-title">{{ article.title }}</h2>
            <p class="post-description">{{ article.summary }}</p>
            <div class="post-meta">
              <span>技术</span>
              <span>·</span>
              <span>{{ formatDate(article.created_at) }}</span>
            </div>
          </div>
        </div>
      </article>
    </div>
  </div>
    </div>
      <Bottom />
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import api from '../../api'
  import Top from '../../components/top.vue'
  import Bottom from '../../components/bottom.vue'
  import { useRouter } from 'vue-router'

  interface Article {
    id: number
    title: string
    summary: string
    created_at: string
  }

  const articles = ref<Article[]>([])
  const router = useRouter()

  const formatDate = (dateString: string): string => {
    const date = new Date(dateString)
    const now = new Date()
    const diffDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24))
    return `${diffDays}天前`
  }

  const fetchArticles = async () => {
    try {
      const response = await api.get('/article/', {
        params: {
          category: 3,  // 技术分类ID
          published: true
        }
      })
      articles.value = response.data
    } catch (error) {
      console.error('获取文章列表失败:', error)
    }
  }

  const goToDetail = (id: number) => {
    router.push(`/tech/${id}`)
  }

  onMounted(() => {
    fetchArticles()
  })
  </script>
  
  <style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Noto+Sans+SC:wght@400;500&display=swap');


.notes {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
.blog-container {
  max-width: 1200px;
  margin: 0 auto;
}

.post-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.post-item {

  padding: 1.5rem;
  padding-left: 0px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.post-item:hover {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-4px);
}

.post-header {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.post-icon {
  width: 20px;
  height: 20px;
  color: #14b8a6;
}

.post-title {
  font-size: 1.25rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  margin-top: 0px;
  color: #333;
}

.post-description {
  font-size: 0.875rem;
  color: #666;
  margin-bottom: 1rem;
}

.post-meta {
  font-size: 0.75rem;
  color: #999;
  display: flex;
  gap: 0.5rem;
}

@media (max-width: 768px) {
  .post-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .post-grid {
    grid-template-columns: 1fr;
  }
}
  
  </style>
  