import { createStore } from "vuex";

export default createStore({
    state() {
        return {
            serverLoader: false,
            serversLoader: false,
        };
      },
      mutations: {
        setServersLoader(state, payload) {
            state.serversLoader = payload;
        }
      },
      getters: {
        getServersLoader(state) {
            return state.serversLoader;
        }
      },
      actions: {
      },
});