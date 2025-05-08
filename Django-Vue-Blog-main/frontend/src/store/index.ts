import { createStore } from 'vuex'

export default createStore({
  state: {
    token: localStorage.getItem('access_token') || '',
    refreshToken: localStorage.getItem('refresh_token') || '',
  },
  mutations: {
    setToken(state, token: string) {
      state.token = token
    },
    setRefreshToken(state, token: string) {
      state.refreshToken = token
    },
    clearTokens(state) {
      state.token = ''
      state.refreshToken = ''
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    }
  },
  actions: {
    logout({ commit }) {
      commit('clearTokens')
    }
  },
  getters: {
    isAuthenticated(state) {
      return !!state.token
    }
  }
}) 