import { createApp } from "vue";
import { createStore } from "vuex";
import App from "./App.vue";

// Vuetify
import "vuetify/styles";
import { createVuetify } from "vuetify";
import "vuetify/styles";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import { library } from "@fortawesome/fontawesome-svg-core";
import { createRouter } from "vue-router";
import { createWebHistory } from "vue-router";
import YouTube from "vue3-youtube";
import axios from "axios";
import VueAxios from "vue-axios";

/* import font awesome icon component */
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

/* import specific icons */
import {
  faUserSecret,
  faHeadphonesSimple,
  faEye,
  faCircleInfo,
  faStar,
  faMusic,
  faGear,
  faList,
  faPeopleGroup,
  faCompactDisc,
  faPlus,
  faPencil,
  faShuffle,
  faTrash,
} from "@fortawesome/free-solid-svg-icons";

library.add(
  faUserSecret,
  faHeadphonesSimple,
  faEye,
  faCircleInfo,
  faStar,
  faMusic,
  faGear,
  faList,
  faPeopleGroup,
  faCompactDisc,
  faPlus,
  faPencil,
  faShuffle,
  faTrash
);

const vuetify = createVuetify({
  components,
  directives,
});

const store = createStore({
  state() {
    return {
      currentVideoPlayTime: 0,
      videoDuration: 0,
      videoTitle: "",
      showPlaylistDialog: false,
      showServersDialog: false,
      user: { id: "86465161", name: `lopasprisijunk`, permissions: 1 },
      selectedServer: null,
      ws: null,
      frontendIP: "FRONT_END_IP",
      backendIP: "BACKEND_IP",
      isAuthenticated: false,
      servers: [],
    };
  },
  mutations: {
    setCurrentVideoPlayTime(state, payload) {
      state.currentVideoPlayTime = payload;
    },
    setVideoDuration(state, payload) {
      state.videoDuration = payload;
    },
    setVideoTitle(state, payload) {
      state.videoTitle = payload;
    },
    toggleShowPlaylistDialog(state) {
      state.showPlaylistDialog = !state.showPlaylistDialog;
    },
    toggleShowServersDialog(state) {
      state.showServersDialog = !state.showServersDialog;
    },
    setUser(state, payload) {
      state.user = payload;
    },
    setSelectedServer(state, payload) {
      state.selectedServer = payload;
    },
    setWs(state, payload) {
      state.ws = payload;
    },
    setIsAuthenticated(state, payload) {
      state.isAuthenticated = payload;
    },
    setServers(state, payload) {
      state.servers = payload;
    },
    RESET_STATE(state) {
      Object.assign(state, getDefaultState());
    },
  },
  getters: {
    getCurrentVideoPlayTime(state) {
      return state.currentVideoPlayTime;
    },
    getVideoDuration(state) {
      return state.videoDuration;
    },
    getVideoTitle(state) {
      return state.videoTitle;
    },
    getShowPlaylistDialog(state) {
      return state.showPlaylistDialog;
    },
    getShowServersDialog(state) {
      return state.showServersDialog;
    },
    getUser(state) {
      return state.user;
    },
    getSelectedServer(state) {
      return state.selectedServer;
    },
    getWs(state) {
      return state.ws;
    },
    getFrontendIP(state) {
      return state.frontendIP;
    },
    getBackendIP(state) {
      return state.backendIP;
    },
    getIsAuthenticated(state) {
      return state.isAuthenticated;
    },
    getServers(state) {
      return state.servers;
    },
    addServer(state) {
      state.servers.push(payload);
    }
  },
  actions: {
    logout({ commit }) {
      commit("RESET_STATE");
    },
  },
});

function getDefaultState() {
  return {
    currentVideoPlayTime: 0,
    videoDuration: 0,
    videoTitle: "",
    showPlaylistDialog: false,
    showServersDialog: false,
    user: { id: "86465161", name: `lopasprisijunk`, permissions: 1 },
    selectedServer: null,
    ws: null,
    frontendIP: "192.168.239.22",
    backendIP: "78.60.244.35", // TODO: DON'T PUSH TO GIT OR JEVGENIJ KILLS U
    isAuthenticated: false,
  };
}

import StreamPage from "./pages/StreamPage.vue";
import FrontPage from "./pages/FrontPage.vue";

const routes = [
  {
    path: "/floor/:id",
    name: "Main",
    meta: {
      requiresAuth: true,
    },
    component: StreamPage,
  },
  { path: "/authentication", name: "Login", component: FrontPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  const isAuthenticated = store.state.isAuthenticated;
  console.log(isAuthenticated);

  if (requiresAuth && !isAuthenticated) {
    next("/authentication");
  } else {
    next();
  }
});

const app = createApp(App);

app.use(store);
app.use(vuetify);
app.use(router);
app.use(VueAxios, axios);
app.component("Youtube", YouTube);
app.component("font-awesome-icon", FontAwesomeIcon);
app.mount("#app");
