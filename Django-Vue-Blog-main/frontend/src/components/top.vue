<template>
  <nav class="top-nav">
    <div class="logo">
      <span class="m-left">◀</span>
      <span class="m">JZH</span>
      <span class="m-right">▶</span>
    </div>
    <div class="nav-links">
      <router-link to="/garden">花园</router-link>
      <router-link to="/now">现在</router-link>
      <router-link to="/about">关于</router-link>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Top'
}
</script>

<style scoped>
.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4rem;
  padding: 0 20px;  /* 添加内边距 */
  box-sizing: border-box;
  max-width: 100%;  /* 确保不超出视口 */
}

.logo {
  display: flex;
  align-items: center;
  font-size: 1.5rem;
  font-weight: bold;
}

.m-left, .m-right {
  color: #00a0e9;
}

.m {
  margin: 0 0.25rem;
}

.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-links a {
  text-decoration: none;
  color: #333;
  font-size: 1rem;
}

.nav-links a:hover {
  color: #00a0e9;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .nav-links {
    gap: 1rem;
  }
  
  .logo {
    font-size: 1.2rem;
  }
}
</style>