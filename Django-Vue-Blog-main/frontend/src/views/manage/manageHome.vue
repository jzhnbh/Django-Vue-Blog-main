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
        <keep-alive>
          <component :is="activeComponent" />
        </keep-alive>
      </el-main>
    </el-container>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, onMounted, markRaw, shallowRef } from 'vue'
  import {
    Document,
    PriceTag,
    ChatDotRound,
    User,
    House
  } from '@element-plus/icons-vue'
  import { useRouter } from 'vue-router'
  import { ElMessage } from 'element-plus'
  import axios from 'axios'
  
  // 直接导入Vue文件
  import ArticleManageVue from './ArticleManage.vue'
  import CategoryManageVue from './CategoryManage.vue'
  import CommentManageVue from './CommentManage.vue'
  import UserManageVue from './UserManage.vue'
  
  export default defineComponent({
    name: 'ManageHome',
    components: {
      Document,
      PriceTag,
      ChatDotRound,
      User,
      House
    },
    setup() {
      const router = useRouter()
      const activeIndex = ref('1')
      
      // 使用shallowRef和markRaw来提高性能
      const activeComponent = shallowRef<any>(markRaw(ArticleManageVue))
      
      const handleSelect = (index: string) => {
        switch(index) {
          case '1':
            activeComponent.value = markRaw(ArticleManageVue)
            break
          case '2':
            activeComponent.value = markRaw(CategoryManageVue)
            break
          case '3':
            activeComponent.value = markRaw(CommentManageVue)
            break
          case '4':
            activeComponent.value = markRaw(UserManageVue)
            break
          case '/home':
            // 首页按钮由goToHome处理
            break
        }
      }
  
      const goToHome = () => {
        router.push('/')
      }

      return {
        activeIndex,
        activeComponent,
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