<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
}
</script>

<style>
body {
  margin: 0;
  padding: 0;
  min-height: 100vh;
  background-image: url('./assets/paper-texture.png');
  background-repeat: repeat;
  background-color: #fafafa;
}

#app {
  font-family: "Noto Serif SC", Georgia, serif;
  min-height: 100vh;
  position: relative;
}

/* 内容容器样式 */
.home, .garden, .now, .about {
  max-width: 1200px;
  margin: 0 auto;
  /* padding: 2rem; */
  position: relative;
}

/* 标题样式 */
h1, h2 {
  font-family: "Ma Shan Zheng", cursive;
  color: #14181b;
}

/* 链接样式 */
a {
  color: #4a5568;
  text-decoration: none;
  transition: color 0.3s ease;
}

a:hover {
  color: #2d3748;
}

/* 全局文本样式 */
p {
  line-height: 1.8;
  color: #050606;
}


/* 添加水印效果 */
.watermark {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) rotate(-45deg);
  font-family: "Ma Shan Zheng", cursive;
  font-size: 120px;
  color: rgba(0,0,0,0.02);
  white-space: nowrap;
  pointer-events: none;
  z-index: 0;
}
</style>
