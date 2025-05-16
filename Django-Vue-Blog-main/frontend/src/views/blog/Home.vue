<template>
  <div class="home">
    <!-- 使用顶部组件 -->
    <Top />

    <!-- 主要内容 -->
    <main class="main-content">
      <h1 class="title">蒋贞宏撰写了有关编程、艺术和社会学的文章。</h1>
      
      <div class="subtitle">
        <p>前端开发者，历史，艺术爱好者</p>
        <p>目前在以下机构担任前端开发 
          <a 
            href="https://www.bsfit.com.cn/" 
            target="_blank" 
            class="highlight"
            @mouseover="hover = true"
            @mouseleave="hover = false"
          >
            BSFIT
            <span class="underline" :class="{ active: hover }"></span>
          </a>
        </p>
      </div>

      <!-- 花园部分 -->
      <section class="garden-section">
        <h2 class="section-title" @click="router.push('/garden')">
          花园 →
          <span class="section-subtitle">数字花园是随着时间的推移慢慢生长的不完美的笔记。</span>
        </h2>
        <p class="garden-desc">
          数字花园是随着时间的推移慢慢生长的不完美的笔记、文章和想法的集合。
          <router-link to="/garden" class="learn-more">了解更多 →</router-link>
        </p>
      </section>

      <!-- 修改文章区域为左右布局 -->
      <div class="content-sections">
        <!-- 左侧论文部分 -->
        <section class="article-section">
          <h2 class="section-title" @click="router.push('/essays')">
            论文 →
            <span class="section-subtitle">有主见、有议程的长篇叙事写作</span>
          </h2>
     
          <div class="article-cards">
            <div 
              v-for="article in paperArticles.slice(0, 2)" 
              :key="article.id" 
              class="article-card"
              @click="goToDetail('essays', article.id)"
            >
              <div class="article-image">
                <img 
                  :src="article.coverimage?.content"
                  :alt="article.title" 
                />
              </div>
              <div class="article-content">
                <h3>{{ article.title }}</h3>
                <p>{{ article.summary }}</p>
                <span class="article-date">{{ formatDate(article.created_at) }}</span>
              </div>
            </div>
          </div>
        </section>

        <!-- 右侧笔记部分 -->
        <section class="notes-section">
          <h2 class="section-title" @click="router.push('/notes')">
            手账 →
            <span class="section-subtitle">对于我还不完全理解的事情，做出松散且不带任何偏见的记录。</span>
          </h2>
          
          <ul class="notes-list">
            <li v-for="article in noteArticles" 
              :key="article.id"
              @click="goToDetail('notes', article.id)"
              class="notes-item"
            >
              <svg class="note-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path 
                  d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" 
                  stroke-width="2" 
                  stroke-linecap="round" 
                  stroke-linejoin="round"
                />
                <path 
                  d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" 
                  stroke-width="2" 
                  stroke-linecap="round" 
                  stroke-linejoin="round"
                />
              </svg>
              <span class="note-title">
                {{ article.title }}
                <span class="title-underline"></span>
              </span>
            </li>
          </ul>
        </section>
      </div>

      <!-- 模式和图书馆部分 -->
      <div class="content-sections second-row">
        <!-- 模式部分 -->
        <section class="patterns-section">
          <h2 class="section-title" @click="router.push('/tech')">
            技术 →
            <span class="section-subtitle">从我自己的观察和研究中收集的设计模式。</span>
          </h2>

          <div class="pattern-list">
            <div 
              v-for="article in techArticles.slice(0, 3)" 
              :key="article.id" 
              class="pattern-item"
              @click="goToDetail('tech', article.id)"
            >
              <div class="pattern-icon">◇</div>
              <div class="pattern-content">
                <h3>{{ article.title }}</h3>
                <p>{{ article.summary }}</p>
                <span class="pattern-date">{{ formatDate(article.created_at) }}</span>
              </div>
            </div>
          </div>
        </section>

        <!-- 图书馆部分 -->
        <section class="library-section">
          <h2 class="section-title" @click="loadCategoryArticles(4)">
            图书馆 →
            <span class="section-subtitle">我读过的书和我喜欢读过的书。</span>
          </h2>
          
          <div class="books-grid">
            <div class="book-card">
              <img src="@/assets/empire-of-pain.jpg" alt="白鹿原" />
              <h3>白鹿原</h3>
              <p>陈忠实</p>
            </div>
            <div class="book-card">
              <img src="@/assets/empire-of-pain.jpg" alt="平凡的世界" />
              <h3>平凡的世界</h3>
              <p>路遥</p>
            </div>
            <div class="book-card">
              <img src="@/assets/empire-of-pain.jpg" alt="资治通鉴" />
              <h3>资治通鉴</h3>
              <p>司马光</p>
            </div>

            <div class="book-card">
              <img src="@/assets/empire-of-pain.jpg" alt="百年孤独" />
              <h3>百年孤独</h3>
              <p>加西亚·马尔克斯</p>
            </div>
          </div>
        </section>
      </div>

      <Bottom />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '../../api'
import { defineComponent } from 'vue'
import Top from '../../components/top.vue'
import Bottom from '../../components/bottom.vue'

interface Article {
  id: number
  title: string
  summary: string
  created_at: string
  category_id: number
  coverimage_id?: number
  coverimage?: {
    content: string
  }
  author: {
    username: string
  }
}

const router = useRouter()
const hover = ref(false)

const articles = ref<Article[]>([])

// 按分类过滤文章
const paperArticles = computed(() => 
  articles.value.filter(article => article.category_id === 1)
)
const noteArticles = computed(() => 
  articles.value.filter(article => article.category_id === 2)
)
const techArticles = computed(() => 
  articles.value.filter(article => article.category_id === 3)
)
const gardenArticles = computed(() => 
  articles.value.filter(article => article.category_id === 4)
)

// 格式化日期
const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  const now = new Date()
  const diffDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24))
  return `${diffDays}天前的文章`
}

// 加载分类文章
const loadCategoryArticles = async (categoryId: number): Promise<void> => {
  try {
    const response = await api.get('/article/', {
      params: { 
        category: categoryId,
        ordering: '-created_at'  // 按创建时间倒序排序
      }
    })
    
    articles.value = response.data
  } catch (error) {
    console.error('加载分类文章失败:', error)
  }
}

// 获取文章列表
const fetchArticles = async () => {
  try {
    const response = await api.get('/article/', {
      params: {
        published: true  // 只获取已发布的文章
      }
    })
    
    // 获取论文文章的封面图
    const articlesWithCover = await Promise.all(
      response.data.map(async (article: Article) => {
        if (article.category_id === 1 && article.coverimage_id) {  // 只处理论文分类
          try {
            const coverResponse = await api.get(`/coverimage/${article.coverimage_id}/`)
            return { ...article, coverimage: coverResponse.data }
          } catch (error) {
            return article
          }
        }
        return article
      })
    )
    
    articles.value = articlesWithCover
  } catch (error) {
    console.error('获取文章列表失败:', error)
  }
}

onMounted(() => {
  fetchArticles()
})

// 跳转到文章详情
const goToDetail = (category: string, id: number) => {
  router.push(`/${category}/${id}`).then(() => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'  // 平滑滚动
    })
  })
}
</script>

<style scoped>
.highlight {
  position: relative;
  text-decoration: none;
  color: inherit;
  transition: transform 0.3s ease, font-size 0.3s ease;
}

.underline {
  position: absolute;
  left: 0;
  right: 0;
  bottom: -2px;
  height: 2px;
  background-color:rgb(91, 197, 247);
  transform: scaleX(0); /* 初始状态下划线不可见 */
  transform-origin: center;
  transition: transform 0.3s ease;
}

.underline.active {
  transform: scaleX(1); /* 鼠标悬停时下划线从中间向两边展开 */
}
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.main-content {
  margin-top: 6rem;
}

.title {
  font-size: 2.5rem;
  font-weight: normal;
  line-height: 1.4;
  margin-bottom: 2rem;
  font-family: "Ma Shan Zheng", cursive;  
  color: #14181b;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

.subtitle {
  font-size: 1.2rem;
  line-height: 1.6;
  color: #14181b;
  margin-bottom: 4rem;
  font-family: "Noto Serif SC", serif;
  opacity: 1;
  font-weight: normal;
}

.highlight {
  color: #00a0e9;
}

.garden-section {
  margin-top: 4rem;
}

.garden-section h2 {
  font-size: 2rem;
  font-weight: normal;
  margin-bottom: 1rem;
  color: #14181b;
  opacity: 1;
}

.garden-desc {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #14181b;
  opacity: 1;
}

.learn-more {
  color: #00a0e9;
  text-decoration: none;
  margin-left: 0.5rem;
}

.learn-more:hover {
  text-decoration: underline;
}

.content-sections {
  margin-top: 6rem;
  display: grid;
  grid-template-columns: 2fr 1fr;  /* 论文部分占据更大空间 */
  gap: 4rem;
}

.article-section {
  padding-right: 2rem;
}

.article-cards {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  display: grid;
  grid-template-columns: 1fr 1fr;  /* 文章卡片左右布局 */
  gap: 2rem;
}

.article-card {
  padding: 2rem;
  background: #cae3ee;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  transition: all 0.3s ease;
}

.article-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.article-image {
  width: 100%;
  height: 300px;
  flex-shrink: 0;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 1.5rem;
}

.article-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.article-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.article-content h3 {
  font-size: 1.4rem;
  font-weight: normal;
  color: #14181b;
  font-family: "Ma Shan Zheng", cursive;
}

.article-content p {
  color: #14181b;
  line-height: 1.6;
}

.article-date {
  color: #14181b;
  font-size: 0.9rem;
  display: block;
  margin-top: 0.5rem;
}

.notes-section {
  margin-top: 0;
  padding-left: 2rem;
  border-left: 1px solid rgba(0, 0, 0, 0.3);
}

.notes-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.notes-item {
  display: flex;
  align-items: center;
  padding: 1rem 0;
  cursor: pointer;
  border-bottom: 1px solid #eee;
  transition: all 0.3s ease;
}

.notes-item:last-child {
  border-bottom: none;
}

.notes-item:hover {
  transform: translateY(-2px);
  padding-left: 10px;
  color: #00a0e9;
}

.note-icon {
  width: 20px;
  height: 20px;
  margin-right: 12px;
  color: #666;
  transition: color 0.3s ease;
}

.notes-item:hover .note-icon {
  color: #00a0e9;
}

.note-title {
  font-size: 1.1rem;
  line-height: 1.4;
  position: relative;
  display: inline-block;
}

.title-underline {
  position: absolute;
  left: 0;
  right: 0;
  bottom: -2px;
  height: 1px;
  background-color: #00a0e9;
  transform: scaleX(0);
  transition: transform 0.3s ease;
  transform-origin: left;
}

.notes-item:hover .title-underline {
  transform: scaleX(1);
}

/* 调整标题样式 */
.section-title {
  font-size: 1.8rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: baseline;
  gap: 1rem;
  color: #14181b;
  opacity: 1;
  font-weight: normal;
  cursor: pointer;
}

.section-subtitle {
  font-size: 1rem;
  color: #14181b;
  font-weight: normal;
  font-family: "Noto Serif SC", serif;
  opacity: 1;
}

.notes-item {
  cursor: pointer;
}

.notes-item:hover {
  color: #00a0e9;
}

/* 响应式布局 */
@media (max-width: 1024px) {
  .content-sections {
    grid-template-columns: 1fr;
    gap: 3rem;
  }
  
  .article-cards {
    grid-template-columns: 1fr;  /* 小屏幕时改为单列 */
  }

  .notes-section {
    padding-left: 0;
    border-left: none;
    border-top: 1px solid rgba(0, 0, 0, 0.1);
    padding-top: 2rem;
  }
}

/* 确保所有标题文字不透明 */
h1, h2, h3 {
  opacity: 1;
  color: #14181b;
}

/* 模式部分样式 */
.second-row {
  margin-top: 6rem;
  display: grid;
  grid-template-columns: 1fr 3fr;  /* 图书馆部分占据 3/4 的空间 */
  gap: 4rem;
}

.pattern-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.pattern-item {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  padding: 0.3rem;
  border-radius: 8px;
  border: 1px solid transparent;  /* 初始透明边框 */
  transition: all 0.3s ease;
  cursor: pointer;
  background-color: transparent;
  transform-style: preserve-3d;  /* 启用3D变换 */
  perspective: 1000px;  /* 设置透视效果 */
}

.pattern-item:hover {
  transform: translateZ(20px);  /* Z轴方向移动 */
  background-color: rgba(0, 160, 233, 0.05);  /* 淡蓝色背景 */
  border-color: rgba(0, 160, 233, 0.2);  /* 显示边框 */
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);  /* 添加阴影增强3D效果 */
}

.pattern-icon {
  font-size: 1.5rem;
  color: #00a0e9;
  margin-top: 1rem;
  transition: transform 0.3s ease;
}

.pattern-item:hover .pattern-icon {
  transform: rotate(45deg);  /* 图标旋转效果 */
}

.pattern-content {
  flex: 1;
}

.pattern-content h3 {
  font-size: 1.2rem;
  margin-bottom: 0.8rem;
  color: #14181b;
  transition: color 0.3s ease;
}

.pattern-content p {
  color: #14181b;
  margin-bottom: 0.8rem;
  line-height: 1.6;
}

.pattern-date {
  font-size: 0.9rem;
  color: #666;
}

.pattern-item:hover .pattern-content h3 {
  color: #00a0e9;  /* 标题变色 */
}

/* 图书馆部分样式 */
.books-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
}

.book-card {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.book-card img {
  width: 100%;
  aspect-ratio: 2/3;
  object-fit: cover;
  border-radius: 4px;
}

.book-card h3 {
  font-size: 1rem;
  color: #14181b;
  margin: 0.5rem 0;
}

.book-card p {
  font-size: 0.9rem;
  color: #14181b;
}

/* 响应式调整 */
@media (max-width: 1024px) {
  .second-row {
    grid-template-columns: 1fr;  /* 小屏幕时改为单列 */
  }
  
  .library-section {
    grid-column: auto;  /* 重置网格列位置 */
  }
  
  .patterns-section {
    grid-column: auto;  /* 重置网格列位置 */
  }

  .books-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .books-grid {
    grid-template-columns: 1fr;
  }
}

.article-card, .pattern-item {
  cursor: pointer;
}

.article-card:hover, .pattern-item:hover {
  transform: translateY(-4px);
  transition: transform 0.3s ease;
}
</style>
