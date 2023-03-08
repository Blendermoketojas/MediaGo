<template>
  <v-row justify="center">
    <v-dialog v-model="this.$store.getters.getShowPlaylistDialog" fullscreen :scrim="false"
      transition="dialog-bottom-transition">
      <v-card color="#373b3e">
        <v-toolbar dark color="#212529" class="position-fixed">
          <v-toolbar-title><span style="color: white">
              <font-awesome-icon icon="fa-solid fa-music" /> Playlist editor</span></v-toolbar-title>
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
            <base-song></base-song>
            <base-song></base-song>
            <base-song></base-song>
            <base-song></base-song>
            <base-song></base-song>
            <base-song></base-song>
            <base-song></base-song>
            <base-song></base-song>
            <base-song></base-song>
            <base-song></base-song>
            <base-song></base-song>
            <base-song></base-song>
            <base-song></base-song>
            <base-song></base-song>
            <base-song></base-song>
            <base-song></base-song>
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
  props: {
  },
  data() {
    return {
      navItems: [{ id: 1, name: "first playlist" }]
    };
  },
  methods: {
    toggleDialog() {
      this.$store.commit('toggleShowPlaylistDialog')
    },
  },
  mounted() {

  }
};
</script>

<style scoped>
ul {
  padding: 0;
  margin-left: 8rem;
}
</style>