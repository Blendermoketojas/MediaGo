<template>
  <v-row justify="center">
    <v-dialog
      v-model="this.$store.getters.getShowPlaylistDialog"
      fullscreen
      :scrim="false"
      transition="dialog-bottom-transition"
    >
      <v-card color="#373b3e">
        <v-toolbar dark color="#212529" class="position-fixed">
          <v-toolbar-title
            ><span style="color: white">
              <font-awesome-icon icon="fa-solid fa-music" /> Playlist
              editor</span
            ></v-toolbar-title
          >
          <v-spacer></v-spacer>
          <v-toolbar-items>
            <v-btn variant="text" color="white" @click="toggleDialog">
              Close
            </v-btn>
          </v-toolbar-items>
        </v-toolbar>
        <div class="d-flex">
          <dialog-sidebar
            :items="navItems"
            :additionVisible="true"
          ></dialog-sidebar>
          <ul class="w-100">
            <new-playlist></new-playlist>
            <VueDraggableNext
              :animation="300"
              tag="base-song"
              :list="ytSongs"
              item-key="title"
              @end="handleChange"
            >
              <base-song
                v-for="(song, index) in ytSongs"
                :key="index"
                :id="'song-' + song.id"
                :title="song.title"
                :duration="song.duration"
                :imgUrl="song.imgUrl"
                :channelTitle="song.channelTitle"
              ></base-song>
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
      songs: [
        { id: 1, link: "jNQXAC9IVRw" },
        { id: 2, link: "YWyHZNBz6FE" },
        { id: 3, link: "t0iZNTsu4Uo" },
      ],
      ytSongs: null,
    };
  },
  methods: {
    handleChange() {
      this.$store.commit("setFirstPlaylistSong", {
        link: `https://www.youtube.com/watch?v=${this.ytSongs[0].link}`,
        duration: this.durationToSeconds(this.ytSongs[0].duration),
        title: this.ytSongs[0].title,
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
    initializePlaylist() {
      const songsArray = this.songs.map((song) => song.link);
      const idsString = this.parseSongsToALine(songsArray);
      const link = `https://www.googleapis.com/youtube/v3/videos?id=${idsString}&key=${this.$store.getters.getYT_API_KEY}&part=snippet,contentDetails&fields=items.snippet(title,thumbnails(default), channelTitle),items.contentDetails(duration)`;
      if (!this.ytSongs) {
        this.$http({
          method: "get",
          url: link,
        })
          .then(
            (response) =>
              (this.ytSongs = response.data.items.map((item, index) => ({
                title: item.snippet.title,
                link: this.songs[index].link,
                duration: this.parseTime(item.contentDetails.duration),
                imgUrl: item.snippet.thumbnails.default.url,
                channelTitle: item.snippet.channelTitle,
              })))
          )
          .then(() =>
            this.$store.commit("setFirstPlaylistSong", {
              link: `https://www.youtube.com/watch?v=${this.ytSongs[0].link}`,
              duration: this.durationToSeconds(this.ytSongs[0].duration),
              title: this.ytSongs[0].title,
            })
          );
      }
    },
  },
  mounted() {
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
          url: `http://${this.$store.getters.getBackendIP}:5000/playlists_get`,
          data: { id: this.$store.getters.getUser.id },
        }).then((songsResponse) =>
          // this.$store.commit("setPlaylists", response.data.playlists);
          console.log(songsResponse.data)
        );
      });
    this.initializePlaylist();
  },
};
</script>

<style scoped>
ul {
  padding: 0;
  margin-left: 8rem;
}
</style>