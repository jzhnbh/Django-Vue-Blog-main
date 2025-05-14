<template>
  <div class="category-manage">
    <h2 style="text-align: center;">分类管理</h2>
    
    <!-- 工具栏 -->
    <el-row class="toolbar">
      <el-col :span="24">
        <el-select
          v-model="selectedCategory"
          placeholder="请选择分类"
          clearable
          @change="handleCategoryChange"
          style="width: 200px; margin-right: 20px;"
        >
          <el-option
            v-for="category in categories"
            :key="category.id"
            :label="category.name"
            :value="category.id"
          />
        </el-select>
        <el-button
          type="primary"
          @click="toggleSortOrder"
        >
          {{ sortOrder === 'asc' ? '正序' : '倒序' }}排序
        </el-button>
      </el-col>
    </el-row>

    <!-- 文章表格 -->
    <el-table :data="filteredArticles" style="width: 100%">
      <!-- 文章标题列(可编辑) -->
      <el-table-column label="文章标题" width="300">
        <template #default="scope">
          <el-input
            v-if="scope.row.isEditing"
            v-model="scope.row.title"
            size="small"
          />
          <span v-else>{{ scope.row.title }}</span>
        </template>
      </el-table-column>

      <!-- 分类列(可编辑) -->
      <el-table-column label="分类" width="200">
        <template #default="scope">
          <el-select 
            v-if="scope.row.isEditing"
            v-model="scope.row.category" 
            size="small"
          >
            <el-option
              v-for="item in categories"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
          <span v-else>
            {{ getCategoryName(scope.row.category_id) }}
          </span>
        </template>
      </el-table-column>

      <!-- 创建时间列 -->
      <el-table-column label="创建时间" width="180">
        <template #default="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>

      <!-- 操作列 -->
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <el-button
            v-if="!scope.row.isEditing"
            type="primary"
            size="small"
            @click="handleEdit(scope.row)"
          >
            编辑
          </el-button>
          <template v-else>
            <el-button
              type="success"
              size="small"
              @click="handleSave(scope.row)"
            >
              保存
            </el-button>
            <el-button
              type="info"
              size="small"
              @click="handleCancel(scope.row)"
            >
              取消
            </el-button>
          </template>
        </template>
      </el-table-column>

      <!-- 更新文章内容列 -->
      <el-table-column label="文章内容" width="120" align="center">
        <template #default="scope">
          <el-button
            type="warning"
            size="small"
            @click="editArticleContent(scope.row)"
          >
            更新内容
          </el-button>
        </template>
      </el-table-column>

      <!-- 删除文章列 -->
      <el-table-column label="删除" width="120" align="center">
        <template #default="scope">
          <el-popconfirm
            title="确认删除这篇文章吗?"
            @confirm="handleDelete(scope.row.id)"
            width="200"
          >
            <template #reference>
              <el-button
                type="danger"
                size="small"
              >
                删除文章
              </el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import api from '../../api'
import { useRouter } from 'vue-router'

interface Article {
  id: number
  title: string
  category: number
  category_id: number
  category_name: string
  created_at: string
  author_name: string
  isEditing?: boolean
}

interface Category {
  id: number
  name: string
  description: string
}

export default defineComponent({
  name: 'CategoryManage',
  setup() {
    const router = useRouter()
    const articles = ref<Article[]>([])
    const categories = ref<Category[]>([])
    const selectedCategory = ref<number | null>(null)
    const sortOrder = ref<'asc' | 'desc'>('desc')

    // 获取所有文章
    const fetchArticles = async () => {
      try {
        const [articleRes, categoryRes] = await Promise.all([
          api.get('/article/'),
          api.get('/category/')
        ])
        
        categories.value = categoryRes.data
        
        // 创建分类 ID 到名称的映射
        const categoryMap = new Map(
          categoryRes.data.map((cat: Category) => [cat.id, cat.name])
        )
        
        // 处理文章数据，添加分类名称
        articles.value = articleRes.data.map((article: any) => ({
          ...article,
          category_name: categoryMap.get(article.category) || '未分类',
          author_name: article.author?.username || '未知作者',
          isEditing: false
        }))
      } catch (error) {
        ElMessage.error('获取数据失败')
        console.error(error)
      }
    }

    // 计算属性
    const filteredArticles = computed(() => {
      let result = articles.value
      
      // 按分类筛选
      if (selectedCategory.value) {
        result = result.filter(article => article.category === selectedCategory.value)
      }

      // 按发布时间排序
      return result.sort((a, b) => {
        const dateA = new Date(a.created_at).getTime()
        const dateB = new Date(b.created_at).getTime()
        return sortOrder.value === 'asc' ? dateA - dateB : dateB - dateA
      })
    })

    // 方法
    const handleCategoryChange = () => {
      // 分类选择变化时自动更新
    }

    const toggleSortOrder = () => {
      sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
    }

    const formatDate = (dateString: string): string => {
      const date = new Date(dateString)
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      }).replace(/\//g, '-')
    }

    // 获取分类名称
    const getCategoryName = (categoryId: number): string => {
      const category = categories.value.find(c => c.id === categoryId)
      return category ? category.name : '未知分类'
    }

    // 处理编辑按钮点击
    const handleEdit = (row: Article) => {
      row.isEditing = true
    }

    // 处理保存按钮点击
    const handleSave = async (row: Article) => {
      try {
        await api.put(`/article/update_meta/${row.id}/`, {
          title: row.title,
          category_id: row.category
        })
        
        // 更新文章的category_id
        const updatedArticle = articles.value.find(a => a.id === row.id)
        if (updatedArticle) {
          updatedArticle.category_id = row.category
          updatedArticle.category = row.category
        }
        
        row.isEditing = false
        ElMessage.success('更新成功')
      } catch (error) {
        console.error('更新文章失败:', error)
        ElMessage.error('更新失败')
      }
    }

    // 添加取消编辑方法
    const handleCancel = (row: Article) => {
      // 恢复原始数据
      const originalArticle = articles.value.find(a => a.id === row.id)
      if (originalArticle) {
        row.title = originalArticle.title
        row.category = originalArticle.category
      }
      row.isEditing = false
    }

    // 跳转到文章编辑页面
    const editArticleContent = (row: Article) => {
      router.push({
        name: 'ArticleManage',
        query: { 
          id: row.id.toString(),
          mode: 'edit'
        }
      })
    }

    // 添加删除文章方法
    const handleDelete = async (id: number) => {
      try {
        await api.delete(`/article/${id}/`)
        ElMessage.success('文章删除成功')
        // 重新获取文章列表
        fetchArticles()
      } catch (error) {
        console.error('删除文章失败:', error)
        ElMessage.error('删除文章失败')
      }
    }

    // 页面加载时获取数据
    onMounted(() => {
      fetchArticles()
    })

    return {
      articles,
      categories,
      selectedCategory,
      sortOrder,
      filteredArticles,
      handleCategoryChange,
      toggleSortOrder,
      formatDate,
      getCategoryName,
      handleEdit,
      handleSave,
      editArticleContent,
      handleCancel,
      handleDelete
    }
  }
})
</script>

<style scoped>
.toolbar {
  margin-bottom: 20px;
}

.category-manage {
  padding: 20px;
}

.el-button {
  margin-right: 10px;
}

.el-input {
  width: 100%;
}

.el-button + .el-button {
  margin-left: 8px;
}
</style>