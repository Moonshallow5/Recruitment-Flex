import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";
import SecureLS from "secure-ls";
//import Ajax from "@/scripts/axios";
// import { useToast } from "vue-toast-notification";
// import "vue-toast-notification/dist/theme-sugar.css";

const ls = new SecureLS({ isCompression: false });

const defaultState = {
  user: {},
  token: null,
  loading: {},
  resetEmail: null,
};

const persistedState = createPersistedState({
  storage: {
    getItem: (key) => ls.get(key),
    setItem: (key, value) => ls.set(key, value),
    removeItem: (key) => ls.remove(key),
  },
});

const state = () => ({ ...defaultState });

const mutations = {
  setUser(state, payload) {
    state.user = payload;
  },
  setToken(state, payload) {
    state.token = payload;
  },
  setLoading(state, payload) {
    state.loading[payload] = true;
  },
  stopLoading(state, payload) {
    state.loading[payload] = false;
  },
  clearLoading(state) {
    state.loading = {};
  },
  resetState(state) {
    Object.assign(state, defaultState);
  },
  setMainLoading(state) {
    state.loading["main"] = true;
  },
  clearMainLoading(state) {
    state.loading["main"] = false;
  },
  setResetEmail(state, email) {
    state.resetEmail = email;
  },
  clearResetEmail(state) {
    state.resetEmail = null;
  },
};

const actions = {
  async login({ commit }, { username, password }) {
    try {
      const Ajax = (await import('@/scripts/axios')).default;
      const response = await Ajax('auth/login', { username, password }, 'POST');
      
      commit('setToken', response.access_token);
      commit('setUser', {
        id: response.user_id,
        username: response.username,
        name: response.name,
        role: response.role,
      });
      
      return response;
    } catch (error) {
      throw error;
    }
  },
  
  async register({ commit }, userData) {
    try {
      const Ajax = (await import('@/scripts/axios')).default;
      const response = await Ajax('auth/register', userData, 'POST');
      return response;
    } catch (error) {
      throw error;
    }
  },
  
  logout({ commit }) {
    commit('resetState');
  },
};

const getters = {
  isAuthenticated: (state) => !!state.token,
  currentUser: (state) => state.user,
  userRole: (state) => state.user?.role || null,
  isApplicant: (state) => state.user?.role === 'applicant',
  isRecruiter: (state) => state.user?.role === 'recruiter',
};

export default createStore({
  plugins: [persistedState],
  state,
  mutations,
  actions,
  getters,
});
