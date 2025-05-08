<template>
  <div class="essays">
    <Top />
    <div class="min-h">
    <!-- Header Section -->
    <div class="max-w-7xl">
      <h1 class="tex">论文</h1>
      <p class="text-xl text-gray-600">有主见、有议程的长篇叙事写作。</p>
    </div>

    <!-- Article Grid Container -->
    <div class="max">
      <div class="grid-container">
        <div 
          v-for="article in articles" 
          :key="article.id"
          class="article-item"
          @click="goToDetail(article.id)"
        >
          <img 
            v-if="coverImages[article.coverimage_id]" 
            :src="coverImages[article.coverimage_id]" 
            :alt="article.title"  
            style="max-width: 100%" 
          />
          <h2 class="t2">{{ article.title }}</h2>
          <p class="text">{{ article.summary }}</p>
          <div class="fle">
            <span>{{ formatDate(article.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
    <Bottom />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api'
import Top from '@/components/top.vue'
import Bottom from '@/components/bottom.vue'
import { useRouter } from 'vue-router'

interface Article {
  id: number
  title: string
  summary: string
  created_at: string
  coverimage_id: number
}

const articles = ref<Article[]>([])
const coverImages = ref<Record<number, string>>({})
const router = useRouter()

// 格式化日期
const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  const now = new Date()
  const diffDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24))
  return `${diffDays}天前的文章`
}

// 获取封面图片URL
const fetchCoverImage = async (id: number) => {
  try {
    const response = await api.get(`/coverimage/${id}/`)
    coverImages.value[id] = response.data.content
  } catch (error) {
    console.error('获取封面图片失败:', error)
  }
}

// 获取论文分类的文章
const fetchArticles = async () => {
  try {
    const response = await api.get('/article/', {
      params: {
        category: 1,  // 论文分类ID
        published: true
      }
    })
    articles.value = response.data

    // 获取所有文章的封面图片
    for (const article of articles.value) {
      if (article.coverimage_id) {
        await fetchCoverImage(article.coverimage_id)
      }
    }
  } catch (error) {
    console.error('获取文章列表失败:', error)
  }
}

const goToDetail = (id: number) => {
  router.push(`/essays/${id}`)
}

onMounted(() => {
  fetchArticles()
})
</script>

<style scoped>
.essays {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(3, auto);
  gap: 2rem;
  overflow: hidden; 
}

.article-item {
  width: 100%;
  max-width: 400px;
  transition: all 0.3s ease;
  overflow: hidden;
  border: 2px solid #ecebeb;
  border-radius: 10px;
  padding: 10px;
}

/* 响应式布局 */
@media (max-width: 1024px) {
  .grid-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .grid-container {
    grid-template-columns: 1fr;
  }
  
  /* 在移动端重置不规则定位 */
  [class*="position-"] {
    transform: none !important;
  }
}

/* 悬停效果 */
.article-item:hover {
  transform: translateY(-5px);
  z-index: 10;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
