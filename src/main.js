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
  faThumbsUp,
  faThumbsDown,
  faListCheck,
  faRightFromBracket,
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
  faTrash,
  faThumbsUp,
  faThumbsDown,
  faListCheck,
  faRightFromBracket
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
      user: {},
      selectedServer: null,
      ws: null,
      frontendIP: "localhost",
      backendIP: "backend_ip",
      YT_API_KEY: "API_KEY",
      isAuthenticated: false,
      servers: null,
      allGenres: null,
      allCountries: null,
      genres: null,
      countries: null,
      pageCount: null,
      isCreationModalShown: false,
      isEditingMode: false,
      firstPlaylistSong: null
    };
  },
  mutations: {
    setIsEditingMode(state, payload) {
      state.isEditingMode = payload;
    },
    setYT_API_KEY(state, payload) {
      state.setYT_API_KEY = payload;
    },
    toggleIsCreationModalShown(state) {
      state.isCreationModalShown = !state.isCreationModalShown;
    },
    setPageCount(state, payload) {
      state.pageCount = payload;
    },
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
    setAllGenres(state, payload) {
      console.log("setAllGenres");
      state.allGenres = payload;
    },
    setAllCountries(state, payload) {
      console.log("setAllCountries");
      state.allCountries = payload;
    },
    addServer(state, payload) {
      console.log(payload);
      state.servers.push(payload);
    },
    setGenres(state, payload) {
      state.genres = payload;
    },
    setCountries(state, payload) {
      state.countries = payload;
    },
    RESET_STATE(state) {
      Object.assign(state, getDefaultState());
    },
    LEAVE_STATE(state) {
      const resetState = serverLeaveState();
      Object.keys(resetState).forEach((key) => {
        state[key] = resetState[key];
      });
    },
    setFirstPlaylistSong(state, payload) {
      state.firstPlaylistSong = payload;
    }
  },
  getters: {
    getFirstPlaylistSong(state) {
      return state.firstPlaylistSong;
    },
    getYT_API_KEY(state) {
      return state.YT_API_KEY;
    },
    getIsEditingMode(state) {
      return state.isEditingMode;
    },
    getIsCreationModalShown(state) {
      return state.isCreationModalShown;
    },
    getPageCount(state) {
      return state.pageCount;
    },
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
    getAllGenres(state) {
      return state.allGenres;
    },
    getAllCountries(state) {
      return state.allCountries;
    },
    getGenres(state) {
      return state.genres;
    },
    getCountries(state) {
      return state.countries;
    },
  },
  actions: {
    logout({ commit }) {
      commit("RESET_STATE");
    },
    leaveServer({ commit }) {
      commit("LEAVE_STATE");
    },
    setAllGenres({ state, commit }) {
      axios
        .get(`http://${state.backendIP}:5000/get_dropdown_create?type=genre`)
        .then((response) => commit("setAllGenres", response.data.data));
    },
    setAllCountries({ state, commit }) {
      axios
        .get(`http://${state.backendIP}:5000/get_dropdown_create?type=country`)
        .then((response) => commit("setAllCountries", response.data.data));
    },
    setServer({ state, commit }, payload) {
      axios
        .get(`http://${state.backendIP}:5000/get_server_info?id=${payload}`)
        .then((response) => commit("setSelectedServer", response.data));
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
    frontendIP: "localhost",
    backendIP: "BACKEND_IP", // TODO: DON'T PUSH TO GIT OR JEVGENIJ KILLS U
    YT_API_KEY: "API_KEY",
    isAuthenticated: false,
    allGenres: null,
    allCountries: null,
    genres: null,
    countries: null,
    pageCount: null,
    isCreationModalShown: false,
    isEditingMode: false,
    firstPlaylistSong: null
  };
}

function serverLeaveState() {
  return {
    currentVideoPlayTime: 0,
    videoDuration: 0,
    videoTitle: "",
    showPlaylistDialog: false,
    showServersDialog: false,
    selectedServer: null,
    ws: null,
    isCreationModalShown: false,
    isEditingMode: false,
    firstPlaylistSong: null
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
