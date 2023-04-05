<template>
  <v-row justify="center">
    <v-dialog v-model="this.$store.getters.getShowPlaylistDialog" fullscreen :scrim="false"
      transition="dialog-bottom-transition">
      <v-card color="#373b3e">
        <v-toolbar dark color="#212529" class="position-fixed">
          <v-toolbar-title><span style="color: white">
              <font-awesome-icon icon="fa-solid fa-music" /> Playlist
              editor</span></v-toolbar-title>
          <v-spacer></v-spacer>
          <v-toolbar-items>
            <v-btn variant="text" color="white" @click="toggleDialog">
              Close
            </v-btn>
          </v-toolbar-items>
        </v-toolbar>
        <div class="d-flex">
          <dialog-sidebar :items="navItems" :additionVisible="true"></dialog-sidebar>
          <ul class="w-100">
            <new-playlist></new-playlist>
            <VueDraggableNext :animation="300" tag="base-song" :list="songsToRender" item-key="title" @end="handleChange">
              <base-song v-for="(song, index) in songsToRender" :key="index" :id="'song-' + song.id" :title="song.title"
                :duration="song.duration" :imgUrl="song.imgUrl" :channelTitle="song.channelTitle"></base-song>
              <span class="display-6 ms-4 text-white" v-if="emptySongList">Playlist is empty.</span>
            </VueDraggableNext>
          </ul>
        </div>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import DialogSidebar from "./playlist_dialog_components/DialogSidebar.vue";
import NewPlaylist from "./NewPlaylist.vue";
import BaseSong from "./playlist_dialog_components/BaseSong.vue";
import { VueDraggableNext } from "vue-draggable-next";
import eventBus from "../../EventBus";

export default {
  components: {
    DialogSidebar,
    NewPlaylist,
    BaseSong,
    VueDraggableNext,
  },
  props: {},
  data() {
    return {
      navItems: [{ id: 1, name: "first playlist" }],
      songs: [],
      ytSongs: [],
      songsToRender: [],
      reqMounted: false,
      emptySongList: false,
    };
  },
  methods: {
    handleChange() {
      this.$store.commit("setFirstPlaylistSong", {
        link: this.songsToRender[0].link,
        duration: this.durationToSeconds(this.songsToRender[0].duration),
        title: this.songsToRender[0].title,
      });
    },
    toggleDialog() {
      this.$store.commit("toggleShowPlaylistDialog");
    },
    parseTime(duration) {
      const match = duration.match(/PT(\d+M)?(\d+S)?/);
      const minutes = match[1] ? parseInt(match[1].slice(0, -1)) : 0;
      const seconds = match[2] ? parseInt(match[2].slice(0, -1)) : 0;
      return `${minutes}:${seconds.toString().padStart(2, "0")}`;
    },
    durationToSeconds(duration) {
      const [minutes, seconds] = duration.split(":");
      const totalSeconds = parseInt(minutes) * 60 + parseInt(seconds);
      return totalSeconds;
    },
    extractVideoId(youtubeUrl) {
      const regex =
        /(?:https?:\/\/)?(?:www\.)?youtu(?:\.be|be\.com)\/(?:watch\?v=)?([A-Za-z0-9_\-]{11})/;
      const match = youtubeUrl.match(regex);
      return match ? match[1] : null;
    },
    parseSongsToALine(array) {
      let result = "";
      for (let i = 0; i < array.length; i++) {
        result += array[i];
        if (i < array.length - 1) {
          result += ",";
        }
      }
      return result;
    },
    initializePlaylist(playlist) {
      const songsArray = playlist.map((song) => this.extractVideoId(song.link));
      const idsString = this.parseSongsToALine(songsArray);
      const link = `https://www.googleapis.com/youtube/v3/videos?id=${idsString}&key=${this.$store.getters.getYT_API_KEY}&part=snippet,contentDetails&fields=items.snippet(title,thumbnails(default), channelTitle),items.contentDetails(duration)`;
      this.$http({
        method: "get",
        url: link,
      }).then((response) => {
        const mappedSongs = response.data.items.map((item, index) => ({
          title: item.snippet.title,
          link: playlist[index].link,
          duration: this.parseTime(item.contentDetails.duration),
          imgUrl: item.snippet.thumbnails.default.url,
          channelTitle: item.snippet.channelTitle,
        }));
        this.ytSongs.push(mappedSongs);
        this.songsToRender = mappedSongs;
      });
    },
    // initializeSelectedPlaylist() {
    //   this.songs = this.$store.getters.getSelectedPlaylist.songs.map((s) => ({
    //     id: s.id,
    //     link: this.extractVideoId(s.link),
    //   }));
    //   this.initializePlaylist(this.songs);
    // },
    getPlaylistsAndSongs() {
      this.$http({
        method: "post",
        url: `http://${this.$store.getters.getBackendIP}:5000/playlists_get`,
        data: { id: this.$store.getters.getUser.id },
      })
        .then((response) => {
          this.$store.commit("setPlaylists", response.data.playlists);
          this.navItems = response.data.playlists;
          this.$store.commit("setSelectedPlaylist", response.data.playlists[0]);
        })
        .then((response) => {
          this.$http({
            method: "post",
            url: `http://${this.$store.getters.getBackendIP}:5000/songs_get`,
            data: {
              id: this.$store.getters.getSelectedPlaylist.id,
              user_id: this.$store.getters.getUser.id,
            },
          }).then((songsResponse) => {
            this.$store.commit("addSongs", {
              playlistId: this.$store.getters.getSelectedPlaylist.id,
              songs: songsResponse.data.songs,
            });
            this.reqMounted = true;
            console.log(songsResponse.data.songs);
            this.initializePlaylist(songsResponse.data.songs);
            console.log("mounted");
          });
        });
    },
  },
  computed: {
    selectedPlaylist() {
      return this.$store.getters.getSelectedPlaylist;
    },
  },
  watch: {
    selectedPlaylist: {
      handler(newVal, oldVal) {
        console.log("changed")
        if (this.reqMounted) {
          const playlist = this.$store.getters.getPlaylists.find(
            (p) => newVal.id === p.id
          );
          if (playlist.songs) {
            this.initializePlaylist(playlist.songs);
            this.emptySongList = false;
          } else {
            this.songsToRender = [];
            this.emptySongList = true;
          }
        }
      },
      immediate: false
    },
  },
  mounted() {
    this.getPlaylistsAndSongs();
    eventBus.on("prepare-playlist", (eventData) => {
      // this.initializeSelectedPlaylist();
    });
  },
  unmounted() {
    eventBus.off("prepare-playlist");
  },
};
</script>

<style scoped>
ul {
  padding: 0;
  margin-left: 8rem;
}
</style>