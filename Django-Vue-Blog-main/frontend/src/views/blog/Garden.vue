<template>
  <div class="garden">
    <Top />
    <div class="min-h">
      <!-- Header Section -->
      <div class="max-w-7xl">
        <h1 class="tex">花园</h1>
        <p class="text-xl text-gray-600">数字花园是随着时间的推移慢慢生长的不完美的笔记。</p>
      </div>

      <!-- Article Grid Container -->
      <div class="blog-container">
        <div class="article-grid">
          <article 
            v-for="article in articles" 
            :key="article.id" 
            class="article-item"
            @click="goToDetail(article.id)"
          >
            <div class="article-header">
              <h2 class="article-title">{{ article.title }}</h2>
              <p class="article-summary">{{ article.summary }}</p>
              <div class="article-meta">
                <span>{{ formatDate(article.created_at) }}</span>
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
        category: 4,  // 花园分类ID
        published: true
      }
    })
    articles.value = response.data
  } catch (error) {
    console.error('获取文章列表失败:', error)
  }
}

const goToDetail = (id: number) => {
  router.push(`/garden/${id}`)
}

onMounted(() => {
  fetchArticles()
})
</script>

<style scoped>
.garden {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.blog-container {
  max-width: 1200px;
  margin: 0 auto;
}

.article-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
}

.article-item {
  padding: 1.5rem;
  border: 1px solid #eaeaea;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.article-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.article-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
  color: #333;
}

.article-summary {
  font-size: 1rem;
  color: #666;
  margin-bottom: 1rem;
  line-height: 1.6;
}

.article-meta {
  font-size: 0.875rem;
  color: #999;
}

@media (max-width: 768px) {
  .article-grid {
    grid-template-columns: 1fr;
  }
}
</style>   