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
          this.$store.commit("setSelectedPlaylist", findPlaylist);
          if (!findPlaylist.songs) {
            this.$http({
              method: "post",
              url: `http://${this.$store.getters.getBackendIP}:5000/songs_get`,
              data: {
                id: findPlaylist.id,
                user_id: this.$store.getters.getUser.id,
              },
            }).then((response) => {
              console.log(response.data);
              this.$store.commit("addSongs", {
                playlistId: findPlaylist.id,
                songs: response.data.songs,
              });
            });
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
