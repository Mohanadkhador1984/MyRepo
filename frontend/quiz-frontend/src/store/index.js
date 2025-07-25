import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    token: localStorage.getItem('token') || '',
    user: {},
  },
  mutations: {
    setToken(state, token) {
      state.token = token
      localStorage.setItem('token', token)
    },
    setUser(state, user) {
      state.user = user
    },
    logout(state) {
      state.token = ''
      state.user = {}
      localStorage.removeItem('token')
    }
  },
  actions: {
    async login({ commit }, credentials) {
      const res = await axios.post('/api/token/', credentials)
      commit('setToken', res.data.access)
    },
    async register(_, credentials) {
      await axios.post('/api/register/', credentials)
    }
  }
})