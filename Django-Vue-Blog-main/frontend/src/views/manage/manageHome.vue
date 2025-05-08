<template>
    <el-container class="manage-container">
      <el-aside width="200px">
        <el-menu
          :default-active="activeIndex"
          class="sidebar-menu"
          @select="handleSelect"
        >
          <el-menu-item index="1">
            <el-icon><Document /></el-icon>
            <span>文章管理</span>
          </el-menu-item>
          <el-menu-item index="2">
            <el-icon><PriceTag /></el-icon>
            <span>分类管理</span>
          </el-menu-item>
          <el-menu-item index="3">
            <el-icon><ChatDotRound /></el-icon>
            <span>评论管理</span>
          </el-menu-item>
          <el-menu-item index="4">
            <el-icon><User /></el-icon>
            <span>用户管理</span>
          </el-menu-item>
            <!-- 添加一个分隔线 -->
    <el-divider class="el-divider"></el-divider>
    
    <!-- 在底部添加回到首页按钮 -->
    <el-menu-item index="/home" @click="goToHome">
      <el-icon><House /></el-icon>
      <span>回到首页</span>
    </el-menu-item>
  </el-menu>

      </el-aside>
     
      <el-main>
        <component :is="currentComponent" />
      </el-main>
    </el-container>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, onMounted } from 'vue'
  import {
    Document,
    PriceTag,
    ChatDotRound,
    User,
    House
  } from '@element-plus/icons-vue'
  import ArticleManage from './ArticleManage.vue'
  import CategoryManage from './CategoryManage.vue'
  import CommentManage from './CommentManage.vue'
  import UserManage from './UserManage.vue'
  import { useRouter } from 'vue-router'
  import { ElMessage } from 'element-plus'
  import axios from 'axios'
  
  export default defineComponent({
    components: {
      Document,
      PriceTag,
      ChatDotRound,
      User,
      ArticleManage,
      CategoryManage,
      CommentManage,
      UserManage,
      House
    },
    setup() {
      const router = useRouter()
      const activeIndex = ref('1')
      const currentComponent = ref('ArticleManage')
  
      const handleSelect = (index: string) => {
        const components = ['ArticleManage', 'CategoryManage', 'CommentManage', 'UserManage']
        currentComponent.value = components[Number(index) - 1]
      }
  
      const goToHome = () => {
  router.push('/')
      }

      return {
        activeIndex,
        currentComponent,
        handleSelect,
        goToHome
      }
    }
  })
  </script>
  
  <style scoped>
  .manage-container {
    height: 100vh;
  }
  
  .side-menu {
    height: 100%;
  }
  
  .el-main {
    padding: 20px;
    background-color: #f5f7fa;
  }
  /* 确保菜单项在底部 */
.sidebar-menu {
  display: flex;
  flex-direction: column;
  height: 100%;
}

/* 分隔线样式 */
.el-divider {
  margin: auto 0 10px 0;
}

/* 回到首页按钮样式 */
.el-menu-item:last-child {
  margin-top: auto;  /* 将按钮推到底部 */
}
  </style>