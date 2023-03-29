<template>
  <li class="nav-item">
    <button
      @click="changeSelectedTab"
      class="nav-link text-white py-3 border-bottom w-100"
      aria-current="page"
      title=""
    >
      <span>
        {{ name }}
      </span>
    </button>
  </li>
</template>

<script>
import eventBus from "../../../EventBus";
export default {
  data() {
    return {};
  },
  methods: {
    changeSelectedTab() {
      this.$store.commit("setDialogSelectedTab", this.name);
      if (this.$store.getters.getCreationModalIs === "playlist") {
        const findPlaylist = this.$store.getters.getPlaylists.find(
          (p) => this.name === p.name
        );
        if (findPlaylist) {
          if (!findPlaylist.songs) {
            this.$http({
              method: "post",
              url: `http://${this.$store.getters.getBackendIP}:5000/songs_get`,
              data: {
                id: findPlaylist.id,
                user_id: this.$store.getters.getUser.id,
              },
            }).then((songsResponse) => {
              this.$store.commit("addSongs", {
                playlistId: findPlaylist.id,
                songs: songsResponse.data.songs,
              });
              this.$store.commit("setSelectedPlaylist", findPlaylist);
              console.log('prepare now')
              eventBus.emit("prepare-playlist", findPlaylist.id);
            });
          } else {
            this.$store.commit("setSelectedPlaylist", findPlaylist);
            eventBus.emit("prepare-playlist", findPlaylist.id);
          }
        }
      }
    },
  },
  props: {
    id: {
      type: Number,
      required: true,
    },
    name: {
      type: String,
      default: "Country playlist",
    },
  },
};
</script>
