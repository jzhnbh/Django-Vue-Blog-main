<template>
    <div class="books">
      <Top />
  
      <!-- Header Section -->
      <div class="header-section">
        <h1 class="title">图书馆</h1>
        <p class="subtitle">我读过的书对我看待世界的方式产生了很大的影响。</p>
      </div>
  
      <!-- Article Grid Container -->
      <div class="book-gallery">
    <div class="book-grid">
      <div v-for="book in books" :key="book.id" class="book-item">
        <div class="book-cover">
          <img 
            :src="book.coverUrl" 
            :alt="book.title"
          />
          <div class="overlay">
            <a 
              v-if="book.googleLink"
              :href="book.googleLink"
              target="_blank"
              rel="noopener noreferrer"
              class="google-link"
            >
              <span>在 Google 上查看</span>
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M7 17L17 7"/>
                <path d="M7 7h10v10"/>
              </svg>
            </a>
          </div>
        </div>
        <div class="book-info">
          <h2>{{ book.title }}</h2>
          <p>{{ book.author }}</p>
        </div>
      </div>
    </div>
  </div>
  
      <Bottom />
    </div>
  </template>
  
  <script>
import Top from '@/components/top.vue'
import Bottom from '@/components/bottom.vue'

const bookCover = '/src/assets/empire-of-pain.jpg'
const bailuyuanCover = '/src/assets/bailuyuan.png'
const zizhitongjianCover = '/src/assets/zizhi.png'
const bainianguduCover = '/src/assets/bainiangudu.png'
  
export default {
  name: 'BookGallery',
  components: {
    Top,
    Bottom
  },
  data() {
    return {
      books: [
        { 
          id: 1, 
          title: '白鹿原', 
          author: '陈忠实', 
          coverUrl: bailuyuanCover, 
          googleLink: 'https://www.google.com/search?q=白鹿原+陈忠实'
        },
        { 
          id: 2, 
          title: '平凡的世界', 
          author: '路遥', 
          coverUrl: bookCover, 
          googleLink: 'https://www.google.com/search?q=平凡的世界+路遥'
        },
        { 
          id: 3, 
          title: '资治通鉴', 
          author: '司马光', 
          coverUrl: zizhitongjianCover, 
          googleLink: 'https://www.google.com/search?q=资治通鉴+司马光'
        },
        { 
          id: 4, 
          title: '百年孤独', 
          author: '加西亚·马尔克斯', 
          coverUrl: bainianguduCover, 
          googleLink: 'https://www.google.com/search?q=百年孤独+加西亚·马尔克斯'
        }
      ]
    }
  }
}
  </script>
  
  <style scoped>
  /* 样式部分保持不变 */
  @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Noto+Sans+SC:wght@400;500&display=swap');
  
  .books {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }
  
  .header-section {
    text-align: center;
    margin-bottom: 3rem;
  }
  
  .title {
    font-size: 2.5rem;
    font-weight: 500;
    color: #2c3e50;
    margin-bottom: 1rem;
    font-family: 'Noto Serif SC', serif;
  }
  
  .subtitle {
    font-size: 1.2rem;
    color: #666;
    line-height: 1.6;
  }
  
  .book-gallery {
    max-width: 1400px;
    margin: 0 auto;
    font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }
  
  .book-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 30px;
    margin: 30px 0;
  }
  
  .book-item {
    display: flex;
    flex-direction: column;
  }
  
  .book-cover {
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .book-cover img {
    width: 100%;
    aspect-ratio: 3/4;
    object-fit: cover;
    display: block;
    transition: all 0.3s ease;
  }
  
  .book-cover:hover img {
    transform: scale(1.05);
    filter: blur(3px);
  }
  
  .overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.3);
    opacity: 0;
    transition: opacity 0.3s ease;
  }
  
  .book-cover:hover .overlay {
    opacity: 1;
  }
  
  .google-link {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: rgba(255, 255, 255, 0.9);
    color: #333;
    padding: 0.5rem 1rem;
    border-radius: 9999px;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    text-decoration: none;
    font-size: 0.875rem;
    opacity: 0;
    transition: all 0.3s ease;
    white-space: nowrap;
  }
  
  .book-cover:hover .google-link {
    opacity: 1;
  }
  
  .google-link:hover {
    background-color: #fff;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .book-info {
    margin-top: 1rem;
  }
  
  .book-info h2 {
    font-family: 'Noto Serif SC', serif;
    font-size: 1rem;
    font-weight: 500;
    margin: 0 0 0.5rem 0;
    line-height: 1.4;
  }
  
  .book-info p {
    font-size: 0.875rem;
    color: #666;
    margin: 0;
  }
  
  @media (max-width: 1200px) {
    .book-grid {
      grid-template-columns: repeat(3, 1fr);
    }
  }
  
  @media (max-width: 768px) {
    .book-grid {
      grid-template-columns: repeat(2, 1fr);
    }
    .book-gallery {
      padding: 0 30px;
    }
  }
  
  @media (max-width: 480px) {
    .book-grid {
      grid-template-columns: 1fr;
    }
    .book-gallery {
      padding: 0 20px;
    }
  }
  </style>