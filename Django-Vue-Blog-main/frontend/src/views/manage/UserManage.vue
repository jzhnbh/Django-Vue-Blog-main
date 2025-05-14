<template>
  <div class="user-manage">
    <h2 style="text-align: center;">用户管理</h2>
    
    <!-- 搜索和操作区域 -->
    <div class="control-area">
      <el-input
        v-model="searchQuery"
        placeholder="搜索用户名或邮箱"
        clearable
        style="width: 300px; margin-right: 15px;"
        @input="handleSearch"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
      
      <el-button type="primary" @click="addNewUser">
        <el-icon><Plus /></el-icon> 新增用户
      </el-button>
    </div>
    
    <!-- 用户列表表格 -->
    <el-table :data="filteredUsers" style="width: 100%; margin-top: 20px;">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="username" label="用户名" width="150" />
      <el-table-column prop="email" label="邮箱" width="200" />
      <el-table-column prop="date_joined" label="注册时间" width="180">
        <template #default="scope">
          {{ formatDate(scope.row.date_joined) }}
        </template>
      </el-table-column>
      <el-table-column prop="last_login" label="最后登录" width="180">
        <template #default="scope">
          {{ scope.row.last_login ? formatDate(scope.row.last_login) : '从未登录' }}
        </template>
      </el-table-column>
      <el-table-column label="管理员" width="100">
        <template #default="scope">
          <el-tag :type="scope.row.is_superuser ? 'danger' : 'info'">
            {{ scope.row.is_superuser ? '是' : '否' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" fixed="right" width="200">
        <template #default="scope">
          <el-button 
            type="primary" 
            size="small" 
            @click="handleEdit(scope.row)"
          >
            编辑
          </el-button>
          <el-popconfirm
            title="确定要删除此用户吗？"
            @confirm="handleDelete(scope.row.id)"
          >
            <template #reference>
              <el-button 
                type="danger" 
                size="small"
                :disabled="scope.row.is_superuser"
              >
                删除
              </el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 用户编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEditing ? '编辑用户' : '新增用户'"
      width="500px"
    >
      <el-form 
        ref="userForm" 
        :model="currentUser" 
        :rules="userRules" 
        label-width="100px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="currentUser.username" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="currentUser.email" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!isEditing">
          <el-input v-model="currentUser.password" type="password" show-password />
        </el-form-item>
        <el-form-item label="管理员权限">
          <el-switch
            v-model="currentUser.is_superuser"
            active-text="是"
            inactive-text="否"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveUser">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import { ref, reactive, computed, onMounted, defineComponent } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, Plus } from '@element-plus/icons-vue'
import api from '../../api'

export default defineComponent({
  name: 'UserManage',
  components: {
    Search,
    Plus
  },
  setup() {
    interface User {
      id: number
      username: string
      email: string
      last_login: string | null
      date_joined: string
      avatar: number | null
      password?: string
      is_superuser: boolean
    }

    // 状态
    const users = ref<User[]>([])
    const searchQuery = ref('')
    const dialogVisible = ref(false)
    const isEditing = ref(false)

    // 当前编辑的用户
    const currentUser = reactive<User>({
      id: 0,
      username: '',
      email: '',
      last_login: null,
      date_joined: '',
      avatar: null,
      is_superuser: false
    })

    // 表单验证规则
    const userRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度不能小于 6 个字符', trigger: 'blur' }
      ]
    }

    // 过滤用户列表
    const filteredUsers = computed(() => {
      if (!searchQuery.value) return users.value

      const query = searchQuery.value.toLowerCase()
      return users.value.filter(user => 
        user.username.toLowerCase().includes(query) || 
        user.email.toLowerCase().includes(query)
      )
    })

    // 格式化日期
    const formatDate = (dateString: string): string => {
      const date = new Date(dateString)
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    // 获取用户列表
    const fetchUsers = async () => {
      try {
        const response = await api.get('/user/')
        // 处理返回的用户数据
        users.value = response.data
      } catch (error) {
        console.error('获取用户列表失败:', error)
        ElMessage.error('获取用户列表失败')
      }
    }

    // 搜索用户
    const handleSearch = () => {
      fetchUsers()
    }

    // 添加新用户
    const addNewUser = () => {
      isEditing.value = false
      Object.assign(currentUser, {
        id: 0,
        username: '',
        email: '',
        last_login: null,
        date_joined: '',
        avatar: null,
        password: '',
        is_superuser: false
      })
      dialogVisible.value = true
    }

    // 编辑用户
    const handleEdit = (user: User) => {
      isEditing.value = true
      Object.assign(currentUser, user)
      currentUser.password = '' // 清空密码字段
      dialogVisible.value = true
    }

    // 删除用户
    const handleDelete = async (userId: number) => {
      try {
        // 找到要删除的用户名
        const userToDelete = users.value.find(user => user.id === userId)
        if (!userToDelete) {
          ElMessage.error('找不到用户')
          return
        }
        await api.delete(`/user/${userToDelete.username}/`)
        ElMessage.success('删除成功')
        fetchUsers() // 刷新用户列表
      } catch (error) {
        console.error('删除用户失败:', error)
        ElMessage.error('删除失败')
      }
    }

    // 保存用户
    const saveUser = async () => {
      // 创建新用户
      if (!isEditing.value) {
        try {
          await api.post('/user/', {
            username: currentUser.username,
            email: currentUser.email,
            password: currentUser.password,
            is_superuser: currentUser.is_superuser
          })
          ElMessage.success('创建用户成功')
          dialogVisible.value = false
          fetchUsers() // 刷新用户列表
        } catch (error) {
          console.error('创建用户失败:', error)
          ElMessage.error('创建用户失败')
        }
      } 
      // 更新现有用户
      else {
        try {
          const updateData: any = {
            username: currentUser.username,
            email: currentUser.email,
            is_superuser: currentUser.is_superuser
          }
          
          // 如果设置了新密码，则更新密码
          if (currentUser.password) {
            updateData.password = currentUser.password
          }
          
          await api.put(`/user/${currentUser.username}/`, updateData)
          ElMessage.success('更新用户成功')
          dialogVisible.value = false
          fetchUsers() // 刷新用户列表
        } catch (error) {
          console.error('更新用户失败:', error)
          ElMessage.error('更新用户失败')
        }
      }
    }

    onMounted(() => {
      fetchUsers()
    })

    return {
      users,
      searchQuery,
      dialogVisible,
      isEditing,
      currentUser,
      userRules,
      filteredUsers,
      formatDate,
      handleSearch,
      addNewUser,
      handleEdit,
      handleDelete,
      saveUser
    }
  }
})
</script>

<style scoped>
.user-manage {
  padding: 20px;
}

.control-area {
  display: flex;
  margin-bottom: 20px;
}

.el-button {
  margin-right: 10px;
}

.el-tag {
  text-align: center;
}
</style> 