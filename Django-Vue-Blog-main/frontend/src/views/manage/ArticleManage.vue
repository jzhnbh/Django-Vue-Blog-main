<template>
  <div class="article-manage">
    <h2 style="text-align: center;">文章管理</h2>
    <div class="editor-container">
      <!-- 标题和概要输入框 -->
      <el-form :model="articleForm" class="article-form">
        <el-form-item label="文章标题" required>
          <el-input 
            v-model="articleForm.title"
            placeholder="请输入文章标题"
          />
        </el-form-item>
        <el-form-item label="文章分类" required>
          <el-select
            v-model="articleForm.category_id"
            placeholder="请选择文章分类"
            @change="handleCategoryChange"
          >
            <el-option
              v-for="tag in tags"
              :key="tag.value"
              :label="tag.label"
              :value="tag.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="文章概要" required>
          <el-input 
            v-model="articleForm.summary"
            type="textarea"
            :rows="3"
            placeholder="请输入文章概要"
          />
        </el-form-item>
        <el-form-item v-if="isPaperCategory" label="文章封面" required>
          <div class="cover-container">
            <!-- 显示当前封面 -->
            <div v-if="previewUrl" class="current-cover">
              <img :src="previewUrl" class="preview-image" />
              <!-- 更新模式下显示删除按钮 -->
              <el-button 
                type="danger" 
                size="small" 
                class="delete-cover" 
                @click="handleDeleteCover"
              >
                重新上传
              </el-button>
            </div>
            
            <!-- 上传区域 -->
            <div 
              v-if="!previewUrl"
              class="upload-area" 
              @click="handleUploadClick"
              role="button"
              tabindex="0"
            >
              <input 
                type="file" 
                ref="fileInput" 
                style="display: none" 
                @change="handleFileChange"
                accept="image/*"
              />
              <div class="upload-content">
                <el-icon class="upload-icon"><Plus /></el-icon>
              </div>
            </div>
          </div>
          <div v-if="isPaperCategory && !articleForm.coverimage" class="avatar-error">
            论文分类必须上传封面
          </div>
        </el-form-item>
      </el-form>

      <!-- 编辑器 -->
      <quill-editor
        v-model:content="editorContent"
        :options="editorOptions"
        contentType="html"
        @update:content="handleContentUpdate"
      />
      
      <!-- 按钮组 -->
      <div class="button-group">
        <el-button 
          type="primary" 
          @click="publishArticle"
        >
          发布文章
        </el-button>
        <el-button 
          type="primary" 
          @click="saveArticle"
        >
          保存文章
        </el-button>
      </div>

      <!-- 实时预览 -->
      <div class="preview-container">
        <div class="preview-sidebar">
          <h3>目录</h3>
          <div class="toc">
            <template v-for="(heading, index) in headings" :key="index">
              <div 
                :class="[
                  'toc-item', 
                  `level-${heading.level}`,
                  { active: currentHeading === heading.id }
                ]"
                @click="scrollToHeading(heading.id)"
              >
                {{ heading.text }}
              </div>
            </template>
          </div>
        </div>
        <div class="preview-content">
          <div class="article-header">
            <h1>{{ articleForm.title }}</h1>
            <div class="article-meta">
              <span class="article-tags" v-if="articleForm.category_id">
                标签：{{ tags.find(tag => tag.value === articleForm.category_id)?.label }}
              </span>
              <span class="article-date">
                {{ new Date().toLocaleDateString() }}
              </span>
            </div>
            <div class="article-summary">
              {{ articleForm.summary }}
            </div>
          </div>
          <div class="article-content" v-html="editorContent"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'
import { ElMessage } from 'element-plus'
import api from '@/api'
import { Plus } from '@element-plus/icons-vue'
import { useRoute } from 'vue-router'

interface ArticleForm {
  title: string;
  summary: string;
  category_id: number | null;
  coverimage: number | null;
  body: string;
}

interface Heading {
  id: string;
  text: string;
  level: number;
}

interface EditorOptions {
  modules: {
    toolbar: any[];
  };
}

// 标签选项
const tags = [
  { label: '论文', value: 1 },
  { label: '手账', value: 2 },
  { label: '技术', value: 3 },
  { label: '花园', value: 4 },
]

// 响应式状态
const editorContent = ref<string>('')
const articleForm = reactive<ArticleForm>({
  title: '',
  summary: '',
  category_id: null,
  coverimage: null,
  body: ''
})
const headings = ref<Heading[]>([])
const currentHeading = ref<string>('')
const previewUrl = ref<string>('')

// 判断是否为论文分类
const isPaperCategory = computed(() => articleForm.category_id === 1)

// 分类改变处理
const handleCategoryChange = (value: number | null): void => {
  if (value !== 1) {
    articleForm.coverimage = null // 如果分类不是论文，清空封面
  }
}

// 编辑器配置
const editorOptions: EditorOptions = {
  modules: {
    toolbar: [
      ['bold', 'italic', 'underline', 'strike'],
      ['blockquote', 'code-block'],
      [{ 'header': [1, 2, 3, false] }],
      [{ 'list': 'ordered'}, { 'list': 'bullet' }],
      [{ 'script': 'sub'}, { 'script': 'super' }],
      [{ 'indent': '-1'}, { 'indent': '+1' }],
      [{ 'direction': 'rtl' }],
      [{ 'size': ['small', false, 'large', 'huge'] }],
      [{ 'color': [] }, { 'background': [] }],
      [{ 'font': [] }],
      ['clean']
    ]
  }
}

// 提取标题
const extractHeadings = (html: string): Heading[] => {
  const div = document.createElement('div')
  div.innerHTML = html
  const headingElements = div.querySelectorAll('h1, h2, h3')
  
  return Array.from(headingElements).map((el, index) => {
    const id = `heading-${index}`
    el.id = id // 添加 ID 以支持锚点跳转
    return {
      id,
      text: el.textContent || '',
      level: parseInt(el.tagName[1])
    }
  })
}

// 内容更新处理
const handleContentUpdate = (content: string): void => {
  headings.value = extractHeadings(content)
}

// 滚动到指定标题
const scrollToHeading = (id: string): void => {
  const element = document.getElementById(id)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
    currentHeading.value = id
  }
}

const fileInput = ref<HTMLInputElement | null>(null)

const handleUploadClick = () => {
  fileInput.value?.click()
}

const handleFileChange = async (event: Event) => {
  const target = event.target as HTMLInputElement
  if (!target.files?.length) return

  const file = target.files[0]
  const formData = new FormData()
  formData.append('content', file)

  try {
    const response = await api.post('/coverimage/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    // 更新 coverimage_id
    articleForm.coverimage = response.data.id
    previewUrl.value = URL.createObjectURL(file)
  } catch (error) {
    console.error('上传封面失败:', error)
    ElMessage.error('上传封面失败')
  }
}

// 发布文章
const publishArticle = async (): Promise<void> => {
  if (!articleForm.title || !articleForm.summary || !editorContent.value || !articleForm.category_id) {
    ElMessage.warning('请填写完整的文章信息')
    return
  }

  if (isPaperCategory.value && !articleForm.coverimage) {
    ElMessage.warning('论文分类必须上传封面')
    return
  }

  const data = {
    title: articleForm.title,
    summary: articleForm.summary,
    body: editorContent.value,
    category_id: articleForm.category_id,
    coverimage_id: articleForm.coverimage,
    toc: headings.value,
    published: true
  }

  const id = route.query.id
  try {
    let response
    
    if (id) {
      response = await api.put(`/article/${id}/`, data)
      ElMessage.success('文章更新成功')
    } else {
      response = await api.post('/article/', data)
      ElMessage.success('文章发布成功')
    }

    // 清空表单
    articleForm.title = ''
    articleForm.summary = ''
    articleForm.category_id = null
    articleForm.coverimage = null
    editorContent.value = ''
    headings.value = []
    previewUrl.value = ''
    
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error(id ? '文章更新失败' : '文章发布失败')
  }
}

// 保存文章
const saveArticle = async (): Promise<void> => {
  const data = {
    title: articleForm.title,
    summary: articleForm.summary,
    body: editorContent.value,
    category_id: articleForm.category_id,
    coverimage_id: articleForm.coverimage,
    toc: headings.value, // 添加目录字段
    punished: false,  // 保存时传递 punished: false
  }

  try {
    // TODO: 调用API保存文章
    const response = await api.post('/article/save/', data)

    if (response.status === 200) {
      ElMessage.success('文章保存成功')
      // 清空表单
      articleForm.title = ''
      articleForm.summary = ''
      articleForm.category_id = null
      articleForm.coverimage = null
      editorContent.value = ''
      headings.value = [] // 清空目录
    }
  } catch (error) {
    ElMessage.error('文章保存失败')
  }
}

const route = useRoute()
const isEditMode = computed(() => route.query.id !== undefined)

// 获取文章数据
const fetchArticle = async () => {
  if (!route.query.id) return
  
  try {
    const response = await api.get(`/article/${route.query.id}/`)
    const article = response.data
    
    articleForm.title = article.title
    articleForm.summary = article.summary
    articleForm.category_id = article.category_id
    articleForm.body = article.body
    editorContent.value = article.body
    
    // 获取封面图片
    if (article.coverimage_id) {
      articleForm.coverimage = article.coverimage_id
      const coverResponse = await api.get(`/coverimage/${article.coverimage_id}/`)
      previewUrl.value = coverResponse.data.content
    }
  } catch (error) {
    console.error('获取文章失败:', error)
    ElMessage.error('获取文章失败')
  }
}

// 删除封面
const handleDeleteCover = () => {
  articleForm.coverimage = null
  previewUrl.value = ''
}

// 更新文章时确保使用最新的 coverimage_id
const updateArticle = async () => {
  try {
    await api.put(`/article/${route.query.id}/`, {
      ...articleForm,
      body: editorContent.value
    })
    ElMessage.success('更新成功')
  } catch (error) {
    console.error('更新失败:', error)
    ElMessage.error('更新失败')
  }
}

// 在组件挂载时获取文章数据
onMounted(() => {
  fetchArticle()
})
</script>

<style scoped>
.article-manage {
  padding: 20px;
}

.editor-container {
  max-width: 1200px;
  margin: 0 auto;
}

.article-form {
  margin-bottom: 20px;
}

.button-group {
  margin: 20px 0;
  display: flex;
  gap: 10px;
}

.preview-container {
  display: flex;
  gap: 30px;
  margin-top: 30px;
  min-height: 600px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  background-color: #fff;
}

.preview-sidebar {
  width: 250px;
  padding: 20px;
  border-right: 1px solid #ebeef5;
  background-color: #f8f9fa;
}

.preview-sidebar h3 {
  margin-bottom: 15px;
  color: #303133;
  font-size: 16px;
}

.toc {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.toc-item {
  cursor: pointer;
  color: #606266;
  line-height: 1.6;
  font-size: 14px;
  transition: all 0.3s ease;
}

.toc-item:hover {
  color: #409EFF;
  padding-left: 5px;
}

.toc-item.active {
  color: #409EFF;
  font-weight: 500;
}

.level-1 {
  font-weight: bold;
}

.level-2 {
  padding-left: 1em;
}

.level-3 {
  padding-left: 2em;
}

.preview-content {
  flex: 1;
  padding: 20px 40px;
  overflow-y: auto;
}

.article-header {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}

.article-header h1 {
  font-size: 28px;
  color: #303133;
  margin-bottom: 15px;
}

.article-meta {
  color: #909399;
  font-size: 14px;
  margin-bottom: 15px;
  display: flex;
  gap: 20px;
}

.article-summary {
  color: #606266;
  font-size: 16px;
  line-height: 1.6;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
  margin-bottom: 20px;
}

.article-content {
  color: #303133;
  font-size: 16px;
  line-height: 1.8;
}

.article-content :deep(h1),
.article-content :deep(h2),
.article-content :deep(h3) {
  margin: 1.5em 0 0.5em;
  color: #303133;
}

.article-content :deep(h1) {
  font-size: 24px;
}

.article-content :deep(h2) {
  font-size: 20px;
}

.article-content :deep(h3) {
  font-size: 18px;
}

.article-content :deep(p) {
  margin: 1em 0;
}

.article-content :deep(blockquote) {
  border-left: 4px solid #409EFF;
  margin: 1em 0;
  padding: 0.5em 1em;
  background-color: #f8f9fa;
}

.article-content :deep(.ql-indent-1) {
  padding-left: 3em;
}

.article-content :deep(.ql-indent-2) {
  padding-left: 6em;
}

:deep(.ql-editor) {
  min-height: 300px;
  font-size: 16px;
  line-height: 1.6;
}

.upload-area {
  width: 150px;
  height: 150px;
  border: 2px dashed #dcdfe6;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: border-color 0.3s;
  overflow: hidden;
}

.upload-area:hover {
  border-color: #409eff;
}

.upload-content {
  text-align: center;
  color: #909399;
}

.upload-icon {
  font-size: 28px;
  margin-bottom: 8px;
}

.avatar-error {
  color: #f56c6c;
  font-size: 12px;
  margin-top: 5px;
}

.summary-avatar-container {
  display: flex;
  gap: 20px;
}

.summary-input {
  flex: 1;
  width: 588px;
}

.avatar-uploader {
  width: 120px;
  height: 120px;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 6px;
}

.cover-container {
  position: relative;
  width: 150px;
}

.current-cover {
  position: relative;
  width: 150px;
  height: 150px;
}

.delete-cover {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  opacity: 0;
  transition: opacity 0.3s;
}

.current-cover:hover .delete-cover {
  opacity: 1;
}
</style>