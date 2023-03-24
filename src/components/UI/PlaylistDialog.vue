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
            <base-song
              v-for="song in ytSongs"
              :title="song.title"
              :duration="song.duration"
              :imgUrl="song.imgUrl"
              :channelTitle="song.channelTitle"
            ></base-song>
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

export default {
  components: {
    DialogSidebar,
    NewPlaylist,
    BaseSong,
  },
  props: {},
  data() {
    return {
      navItems: [{ id: 1, name: "first playlist" }],
      songs: [
        { id: 1, link: "gG_dA32oH44" },
        { id: 2, link: "YWyHZNBz6FE" },
        { id: 3, link: "t0iZNTsu4Uo" },
      ],
      ytSongs: null,
    };
  },
  methods: {
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

      // Loop through the array
      for (let i = 0; i < array.length; i++) {
        result += array[i];
        if (i < array.length - 1) {
          result += ",";
        }
      }
      return result;
    },
  },
  mounted() {
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
            (this.ytSongs = response.data.items.map((item) => ({
              title: item.snippet.title,
              duration: this.parseTime(item.contentDetails.duration),
              imgUrl: item.snippet.thumbnails.default.url,
              channelTitle: item.snippet.channelTitle,
            })))
        )
        .then(() =>
          this.$store.commit("setFirstPlaylistSong", { link: `https://www.youtube.com/watch?v=${this.songs[0].link}`,duration: this.durationToSeconds(this.ytSongs[0].duration), title: this.ytSongs[0].title })
        );
    }
  },
};
</script>
<!-- channelTitle:"KanyeWestVEVO"
duration:"4:12"
imgUrl:"https://i.ytimg.com/vi/gG_dA32oH44/default.jpg"
title:"Jay-Z & Kanye West - Ni**as In Paris (Explicit)" -->


<style scoped>
ul {
  padding: 0;
  margin-left: 8rem;
}
</style>