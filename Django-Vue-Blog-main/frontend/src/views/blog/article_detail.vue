<template>
  <div class="article-detail">
    <Top />
    
    <main class="main-content">
      <!-- 标题部分使用居中布局 -->
      <div class="header-container">
        <div class="category-indicator">
          <span class="category-text">{{ getCategoryName(article.category_id) }}</span>
          <span class="download-icon">↓</span>
        </div>
        <div class="article-header">
          <h1>{{ article.title }}</h1>
          <p class="article-description">{{ article.summary }}</p>
          <div class="article-meta">
            <div class="tags">
              <span 
                v-for="tag in article.tags" 
                :key="tag"
                class="tag"
              >{{ tag }}</span>
            </div>
            <span class="publish-time">{{ formatDate(article.created_at) }}种植</span>
          </div>
        </div>
      </div>

      <!-- 内容区域撑满屏幕 -->
      <div class="content-container">
        <div class="content-wrapper">
          <!-- 左侧目录 -->
          <div class="sidebar">
            <div class="toc" v-if="hasToc">
              <div class="toc-header">
                <span class="toc-icon">≡</span>
                <span class="toc-title">目录</span>
              </div>
              <div class="toc-items">
                <div 
                  v-for="(heading, index) in article.toc" 
                  :key="index"
                  :class="[
                    'toc-item', 
                    `level-${heading.level}`,
                    { active: currentHeading === heading.id }
                  ]"
                  @click="scrollToHeading(heading.id)"
                >
                  {{ heading.text }}
                </div>
              </div>
            </div>
          </div>

          <!-- 中间文章内容 -->
          <div class="article-main">
            <!-- 文章主体内容 -->
            <article class="article-content" v-html="compiledMarkdown"></article>

            <!-- 文章底部互动区域 -->
            <div class="interaction-section">
              <div class="interaction-header">
                <div class="like-container">
                  <div 
                    class="like-button" 
                    :class="{ 'liked': isLiked }"
                    @click="handleLike"
                  >
                    <svg 
                      class="heart-icon" 
                      viewBox="0 0 24 24" 
                      fill="none" 
                      stroke="currentColor"
                    >
                      <path 
                        d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" 
                        :fill="isLiked ? 'currentColor' : 'none'"
                        stroke-width="2"
                      />
                    </svg>
                  </div>
                  <span class="like-count">{{ likeCount }}</span>
                </div>
                <span class="comment-count">{{ comments.length }} 条评论</span>
              </div>

              <!-- 评论区域 -->
              <div class="comment-section">
                <!-- 评论输入框 -->
                <div class="comment-input">
                  <el-input
                    v-model="newComment"
                    type="textarea"
                    :rows="3"
                    placeholder="写下你的评论..."
                  />
                  <el-button 
                    type="primary" 
                    @click="submitComment"
                    :disabled="!newComment.trim()"
                  >
                    发表评论
                  </el-button>
                </div>

                <!-- 评论列表 -->
                <div class="comment-list">
                  <div v-for="comment in comments" :key="comment.id" class="comment-item">
                    <div class="comment-header">
                      <span class="username">{{ comment.user.username }}</span>
                      <span class="time">{{ formatDate(comment.created_at) }}</span>
                    </div>
                    <div class="comment-content">{{ comment.content }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 右侧空白区域 -->
          <div class="right-sidebar"></div>
        </div>
      </div>
    </main>

    <Bottom />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { marked } from 'marked'
import api from '@/api'
import Top from '@/components/top.vue'
import Bottom from '@/components/bottom.vue'
import { ElMessage } from 'element-plus'
import { Star, StarFilled } from '@element-plus/icons-vue'

interface Article {
  id: number
  title: string
  body: string
  created_at: string
  category_id: number
  summary: string
  toc: Array<{ id: string; text: string; level: number }>
  tags: Array<string>
  coverimage_id: number | null
  body_html: string
  toc_html: string
  author: {
    id: number
    username: string
  }
}

interface Comment {
  id: number
  content: string
  created_at: string
  user: {
    username: string
  }
}

interface ErrorResponse {
  response?: {
    data: {
      [key: string]: string[]
    }
  }
}

const route = useRoute()
const article = ref<Article>({
  id: 0,
  title: '',
  body: '',
  created_at: '',
  category_id: 0,
  summary: '',
  toc: [],
  tags: [],
  coverimage_id: null,
  body_html: '',
  toc_html: '',
  author: {
    id: 0,
    username: ''
  }
})
const currentHeading = ref('')
const comments = ref<Comment[]>([])
const newComment = ref('')
const isLiked = ref(false)
const likeCount = ref(0)
const isLoggedIn = ref(false) // 根据你的登录状态设置
const previewUrl = ref('')

const compiledMarkdown = computed(() => {
  return marked(article.value.body)
})

const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// 分类字典
const categories: { [key: number]: string } = {
  1: '论文',
  2: '手账',
  3: '技术',
  4: '花园'
}

// 获取分类名称
const getCategoryName = (categoryId: number): string => {
  return categories[categoryId] || '未知分类'
}

const scrollToHeading = (id: string) => {
  const element = document.getElementById(id)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
    currentHeading.value = id
  }
}

const fetchArticle = async () => {
  try {
    const response = await api.get(`/article/${route.params.id}/`)
    article.value = response.data
    
    // 获取封面图片
    if (article.value.coverimage_id) {
      const coverResponse = await api.get(`/coverimage/${article.value.coverimage_id}/`)
      previewUrl.value = coverResponse.data.content
    }

    // 在文章数据获取成功后，再获取评论和点赞数据
    await Promise.all([
      fetchComments(),
      fetchLikeStatus()
    ])
  } catch (error) {
    console.error('获取文章失败:', error)
    ElMessage.error('获取文章失败')
  }
}

// 判断是否有目录
const hasToc = computed(() => {
  return article.value.toc && article.value.toc.length > 0
})

// 获取评论列表
const fetchComments = async () => {
  try {
    const response = await api.get(`/article/${route.params.id}/comments/`)  // 使用路由参数
    comments.value = response.data
  } catch (error) {
    console.error('获取评论失败:', error)
    ElMessage.error('获取评论失败')
  }
}

// 从 JWT token 中获取用户 ID
const getUserIdFromToken = (token: string): number | null => {
  try {
    const base64Url = token.split('.')[1]
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
    const payload = JSON.parse(window.atob(base64))
    return payload.user_id
  } catch (error) {
    return null
  }
}

// 提交评论
const submitComment = async () => {
  if (!newComment.value.trim()) return
  
  const token = localStorage.getItem('access_token')
  if (!token) {
    ElMessage.warning('请先登录')
    return
  }

  try {
    await api.post(`/comment/`, {
      article: article.value.id,  // 使用 article 而不是 article_id
      content: newComment.value,
      parent_id: null
    })
    
    ElMessage.success('评论成功')
    newComment.value = ''
    await fetchComments()
  } catch (error: unknown) {
    console.error('发表评论失败:', error)
    const err = error as ErrorResponse
    if (err.response?.data) {
      ElMessage.error(Object.values(err.response.data)[0][0] || '发表评论失败')
    } else {
      ElMessage.error('发表评论失败')
    }
  }
}

// 处理点赞
const handleLike = async () => {
  try {
    if (isLiked.value) {
      await api.delete(`/article/${article.value.id}/like/`)
      likeCount.value--
    } else {
      await api.post(`/article/${article.value.id}/like/`)
      likeCount.value++
    }
    isLiked.value = !isLiked.value
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
  }
}

// 获取点赞状态和数量
const fetchLikeStatus = async () => {
  try {
    const response = await api.get(`/article/${route.params.id}/like/`)  // 使用路由参数
    isLiked.value = response.data.is_liked
    likeCount.value = response.data.like_count
  } catch (error) {
    console.error('获取点赞状态失败:', error)
  }
}

onMounted(() => {
  fetchArticle()  // 只需要调用 fetchArticle
})
</script>

<style scoped>
.article-detail {
  box-sizing: border-box;  /* 关键：确保padding计入总宽度 */
  width: 100%;
  padding: 20px 40px;  /* 使用padding代替margin */
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.content-container {
  width: 100%;
  box-sizing: border-box;
}

.content-wrapper {
  display: grid;
  grid-template-columns: 250px minmax(0, 1fr) 250px;  /* 三列布局 */
  gap: 40px;
  max-width: 1600px;
  margin: 0 auto;
}

/* 分类标识样式 */
.category-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
}

.category-text {
  color: #e91e63;
  font-size: 0.9em;
}

.download-icon {
  color: #1976d2;
  cursor: pointer;
}

/* 文章头部样式 */
.article-header {
  margin-bottom: 60px;
  text-align: center;
  max-width: 800px;
  margin: 0 auto 60px;
}

.article-header h1 {
  font-size: 2.5em;
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 20px;
  line-height: 1.3;
}

.article-description {
  font-size: 1.1em;
  color: #666;
  line-height: 1.6;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.article-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 30px;
}

.tags {
  display: flex;
  gap: 10px;
}

.tag {
  color: #e91e63;
  font-size: 0.9em;
  padding: 2px 8px;
  border-radius: 4px;
  background-color: rgba(233, 30, 99, 0.1);
}

.publish-time {
  color: #666;
  font-size: 0.9em;
}

/* 目录样式 */
.sidebar, .right-sidebar {
  position: sticky;
  top: 20px;
  height: fit-content;
  width: 100%;
}

.toc {
  font-size: 0.9em;
  max-width: 230px;  /* 限制目录最大宽度 */
}

.toc-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
  color: #2c3e50;
}

.toc-icon {
  font-size: 1.2em;
}

.toc-title {
  font-weight: 500;
}

.toc-items {
  display: flex;
  flex-direction: column;
  gap: 8px;  /* 减小目录项间距 */
}

.toc-item {
  cursor: pointer;
  color: #666;
  line-height: 1.4;
  transition: all 0.2s ease;
  overflow: hidden;
  text-overflow: ellipsis;  /* 文字过长时显示省略号 */
  white-space: nowrap;  /* 防止文字换行 */
}

.toc-item:hover {
  color: #1976d2;
}

.toc-item.active {
  color: #1976d2;
}

.level-1 {
  font-weight: 500;
}

.level-2 {
  padding-left: 1.2em;
  font-size: 0.95em;
}

.level-3 {
  padding-left: 2.4em;
  font-size: 0.9em;
}

/* 文章内容样式 */
.article-content {
  width: 100%;
  max-width: none;
  margin: 0;
  font-size: 1.1em;
  line-height: 1.8;
  color: #2c3e50;
}

.article-content :deep(h1),
.article-content :deep(h2),
.article-content :deep(h3) {
  margin: 2em 0 1em;
  font-weight: 500;
  line-height: 1.4;
}

.article-content :deep(h1) {
  font-size: 1.8em;
}

.article-content :deep(h2) {
  font-size: 1.5em;
}

.article-content :deep(h3) {
  font-size: 1.3em;
}

.article-content :deep(p) {
  margin: 1.2em 0;
}

.article-content :deep(img) {
  max-width: 100%;
  border-radius: 8px;
  margin: 2em 0;
}

/* 响应式布局 */
@media (max-width: 1400px) {
  .content-wrapper {
    grid-template-columns: 250px 1fr;  /* 隐藏右侧边栏 */
  }
  .right-sidebar {
    display: none;
  }
}

@media (max-width: 1024px) {
  .content-wrapper {
    grid-template-columns: 1fr;  /* 单列布局 */
  }
  .sidebar {
    display: none;
  }
}

@media (max-width: 768px) {
  .article-header h1 {
    font-size: 2em;
  }

  .article-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .article-detail {
    padding: 0 20px;  /* 在小屏幕上减小padding */
  }
}

.article-main {
  flex: 1;
  min-width: 200px;
}

.interaction-section {
  margin-top: 60px;
  padding-top: 40px;
  border-top: 1px solid #eee;
}

.interaction-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
}

.like-container {
  display: flex;
  align-items: center;
  gap: 8px;
}

.like-button {
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  transition: all 0.3s ease;
  color: #666;
  background: transparent;
}

.like-button:hover {
  background: rgba(0, 0, 0, 0.05);
}

.like-button.liked {
  color: #409EFF;
  animation: like-animation 0.3s ease;
}

.heart-icon {
  width: 24px;
  height: 24px;
}

.like-count {
  font-size: 1rem;
  color: #666;
  min-width: 24px;
}

@keyframes like-animation {
  0% { transform: scale(1); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

.comment-count {
  color: #666;
  font-size: 0.9em;
}

.comment-section {
  margin-top: 30px;
}

.comment-input {
  margin-bottom: 30px;
}

.comment-input .el-button {
  margin-top: 10px;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.comment-item {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.username {
  font-weight: 500;
  color: #333;
}

.time {
  color: #999;
  font-size: 0.9em;
}

.comment-content {
  color: #333;
  line-height: 1.6;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .interaction-section {
    margin-top: 40px;
    padding: 20px;
  }
}
</style> 