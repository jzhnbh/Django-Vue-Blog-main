<template>
  <footer class="footer-section">
    <div class="footer-nav">
      <div class="social-links">
        <div class="social-icons">
          <a href="https://github.com/jzhnbh" class="social-link">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2C6.477 2 2 6.477 2 12C2 16.991 5.657 21.128 10.438 22.279C11.063 22.394 11.25 21.993 11.25 21.643V19.964C7.727 20.622 7.312 18.791 7.312 18.791C7 17.607 6.375 17.307 6.375 17.307C5.562 16.693 6.438 16.693 6.438 16.693C7.375 16.764 7.813 17.75 7.813 17.75C8.688 19.107 10.125 18.821 11.25 18.536C11.313 17.857 11.625 17.393 11.938 17.143C9.0625 16.893 6.063 15.993 6.063 11.857C6.063 10.714 6.438 9.786 7.063 9.071C6.938 8.786 6.688 7.679 7.188 6.293C7.188 6.293 8.188 6.007 10.688 7.643C11.438 7.429 12.313 7.321 13.188 7.321C14.063 7.321 14.938 7.429 15.688 7.643C18.188 6.007 19.188 6.293 19.188 6.293C19.688 7.679 19.438 8.786 19.313 9.071C19.938 9.786 20.313 10.714 20.313 11.857C20.313 15.993 17.313 16.893 14.438 17.143C14.813 17.464 15.188 18.107 15.188 19.071V21.643C15.188 21.993 15.375 22.394 16 22.279C20.781 21.128 24.438 16.991 24.438 12C24.438 6.477 19.961 2 14.438 2H12Z" fill="currentColor"/>
            </svg>
          </a>
          <a href="#" class="social-link">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M20 4H4C2.9 4 2.01 4.9 2.01 6L2 18C2 19.1 2.9 20 4 20H20C21.1 20 22 19.1 22 18V6C22 4.9 21.1 4 20 4ZM20 8L12 13L4 8V6L12 11L20 6V8Z" fill="currentColor"/>
            </svg>
          </a>
        </div>
        <div class="copyright">
          © 2025 蒋贞宏
        </div>
      </div>
      
      <div class="site-links">
        <div class="links-column">
          <router-link to="/tech">技术</router-link>
          <router-link to="/books">图书</router-link>
        </div>
        <div class="links-column">
          <router-link to="/essays">论文</router-link>
          <router-link to="/notes">手账</router-link>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Bottom'
}
</script>

<style scoped>
.footer-section {
  margin-top: 4rem;
  padding: 4rem 20px 0;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
  max-width: 100%;
}

.footer-nav {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 2rem;
  margin-bottom: 4rem;
  max-width: 1600px;
  margin: 0 auto;
}

.social-links {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 1rem;
}

.social-icons {
  display: flex;
  gap: 1.5rem;
}

.social-link {
  color: #14181b;
  text-decoration: none;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.3s ease;
}

.social-link:hover {
  color: #00a0e9;
}

.site-links {
  display: flex;
  gap: 4rem;
  margin-left: auto;
}

.links-column {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.links-column a {
  color: #14181b;
  text-decoration: none;
  font-size: 1rem;
}

.links-column a:hover {
  color: #00a0e9;
}

.copyright {
  margin-top: 1rem;
  color: #666;
  font-size: 0.9rem;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .footer-nav {
    flex-direction: column;
    gap: 2rem;
  }
  
  .social-links {
    align-items: flex-start;
  }
  
  .site-links {
    margin-left: 0;
  }
}
</style>
