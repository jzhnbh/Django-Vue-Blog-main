declare module '*.vue' {
    import { DefineComponent } from 'vue';
    const component: DefineComponent<{}, {}, any>;
    export default component;
  }
  declare module '@/store' {

    import { Store } from 'vuex'
  
    const store: Store<any>
  
    export default store
  
  } 
  declare module '@/api' {
    import { AxiosInstance } from 'axios'
    const api: AxiosInstance
    export default api
  }

declare module 'vue-cropper' {
  import { Component } from 'vue'
  export const VueCropper: Component
}