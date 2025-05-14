<template>
  <div class="comment-manage">
    <h2 style="text-align: center;">评论与数据统计</h2>

    <!-- 文章列表及其统计数据 -->
    <el-table :data="articles" style="width: 100%">
      <!-- 文章标题列 -->
      <el-table-column label="文章标题" prop="title" min-width="200">
        <template #default="scope">
          <el-link type="primary" @click="showComments(scope.row)">
            {{ scope.row.title }}
          </el-link>
        </template>
      </el-table-column>

      <!-- 统计数据列 -->
      <el-table-column label="统计数据" width="200">
        <template #default="scope">
          <div class="stats">
            <el-tooltip content="点赞数">
              <span class="stat-item">
                <el-icon><Star /></el-icon>
                {{ scope.row.likes_count }}
              </span>
            </el-tooltip>
            <el-tooltip content="浏览量">
              <span class="stat-item">
                <el-icon><View /></el-icon>
                {{ scope.row.views_count }}
              </span>
            </el-tooltip>
            <el-tooltip content="评论数">
              <span class="stat-item">
                <el-icon><ChatLineRound /></el-icon>
                {{ scope.row.comments_count }}
              </span>
            </el-tooltip>
          </div>
        </template>
      </el-table-column>

      <!-- 发布时间列 -->
      <el-table-column 
        label="发布时间" 
        prop="created_at" 
        width="180"
        :formatter="formatDate"
      />
    </el-table>

    <!-- 评论详情对话框 -->
    <el-dialog 
      v-model="dialogVisible" 
      :title="currentArticle ? `《${currentArticle.title}》的评论` : '评论'"
      width="70%"
    >
      <el-table :data="comments" style="width: 100%">
        <el-table-column label="评论内容" prop="content" min-width="300" />
        <el-table-column label="评论者" prop="user.username" width="120" />
        <el-table-column 
          label="评论时间" 
          prop="created_at" 
          width="180"
          :formatter="formatDate"
        />
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="scope">
            <el-popconfirm
              title="确定要删除这条评论吗？"
              @confirm="deleteComment(scope.row.id)"
            >
              <template #reference>
                <el-button type="danger" size="small">删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import { ref, onMounted, defineComponent } from 'vue'
import { ElMessage } from 'element-plus'
import { Star, View, ChatLineRound } from '@element-plus/icons-vue'
import api from '../../api'

interface Article {
  id: number
  title: string
  created_at: string
  likes_count: number
  views_count: number
  comments_count: number
}

interface Comment {
  id: number
  content: string
  created_at: string
  user: {
    username: string
  }
}

export default defineComponent({
  name: 'CommentManage',
  components: {
    Star,
    View,
    ChatLineRound
  },
  setup() {
    const articles = ref<Article[]>([])
    const comments = ref<Comment[]>([])
    const dialogVisible = ref(false)
    const currentArticle = ref<Article | null>(null)

    // 获取文章列表及统计数据
    const fetchArticles = async () => {
      try {
        const response = await api.get('/article/stats/')
        articles.value = response.data
      } catch (error) {
        console.error('获取文章统计数据失败:', error)
        ElMessage.error('获取数据失败')
      }
    }

    // 获取文章评论
    const showComments = async (article: Article) => {
      currentArticle.value = article
      try {
        const response = await api.get(`/article/${article.id}/comments/`)
        comments.value = response.data
        dialogVisible.value = true
      } catch (error) {
        console.error('获取评论失败:', error)
        ElMessage.error('获取评论失败')
      }
    }

    // 删除评论
    const deleteComment = async (commentId: number) => {
      try {
        await api.delete(`/comment/${commentId}/`)
        ElMessage.success('删除成功')
        if (currentArticle.value) {
          showComments(currentArticle.value) // 刷新评论列表
        }
      } catch (error) {
        console.error('删除评论失败:', error)
        ElMessage.error('删除失败')
      }
    }

    // 格式化日期
    const formatDate = (row: any, column: any, cellValue: string) => {
      const date = new Date(cellValue)
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    onMounted(() => {
      fetchArticles()
    })

    return {
      articles,
      comments,
      dialogVisible,
      currentArticle,
      showComments,
      deleteComment,
      formatDate
    }
  }
})
</script>

<style scoped>
.comment-manage {
  padding: 20px;
}

.stats {
  display: flex;
  gap: 15px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #606266;
}

.el-icon {
  font-size: 16px;
}
</style> 