declare module '@/components/*.vue' {
  import { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

declare module '@/api' {
  import { AxiosInstance } from 'axios'
  const api: AxiosInstance
  export default api
} 