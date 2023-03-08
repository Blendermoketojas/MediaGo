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
import { createRouter } from 'vue-router';
import { createWebHistory } from "vue-router";
import YouTube from 'vue3-youtube'
import axios from 'axios'
import VueAxios from 'vue-axios'

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
  faTrash

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
      videoTitle: '',
      showPlaylistDialog: false,
      showServersDialog: false,
      user: { id: '86465161', name: "tadelis123", permissions: 1 },
      selectedServer: null,
      ws: null,
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
    }
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
    }
  }
});

import StreamPage from './pages/StreamPage.vue'
import FrontPage from './pages/FrontPage.vue'

const routes = [
  { path: '/floor/:id', component: StreamPage },
  { path: '/authentication', component: FrontPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const app = createApp(App);

app.use(store);
app.use(vuetify);
app.use(router);
app.use(VueAxios, axios);
app.component('Youtube', YouTube);
app.component("font-awesome-icon", FontAwesomeIcon);
app.mount("#app");
