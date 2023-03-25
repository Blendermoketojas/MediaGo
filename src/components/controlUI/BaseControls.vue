<template>
  <div class="d-flex flex-row justify-content-center">
    <base-card>
      <button
        :disabled="isDisabled"
        @click="addSongToQueue"
        type="button"
        class="btn blue-thumb"
      >
        <font-awesome-icon icon="fa fa-music"></font-awesome-icon> Play a song
      </button>
    </base-card>
    <div class="dj-table"></div>
    <base-card
      class="d-flex flex-column justify-content-center align-items-center"
    >
      <div class="mb-4">
        <button type="button" class="fs-3 me-5 green-thumb">
          <font-awesome-icon icon="fa fa-thumbs-up"></font-awesome-icon>
        </button>
        <button type="button" class="fs-3 me-5 red-thumb">
          <font-awesome-icon icon="fa fa-thumbs-down"></font-awesome-icon>
        </button>
        <button type="button" class="fs-3 blue-thumb">
          <font-awesome-icon icon="fa fa-plus"></font-awesome-icon>
        </button>
      </div>
      <v-progress-linear
        class="me-4"
        style="width: 90%; background-color: crimson"
        color="green"
        model-value="35"
      ></v-progress-linear>
    </base-card>
  </div>
</template>

<script>
import BaseCard from "../UI/BaseCard.vue";
import { mapGetters } from "vuex";
export default {
  computed: {
    ...mapGetters([
      "getWs",
      "getSelectedServer",
      "getUser",
      "getFirstPlaylistSong",
    ]),
  },
  data() {
    return {
      isDisabled: false,
    };
  },
  components: {
    BaseCard,
  },
  methods: {
    addSongToQueue() {
      if (this.getSelectedServer) {
        const response = {
          type: "addToQueue",
          username: this.getUser.name,
          userId: this.getUser.id,
          roomId: this.getSelectedServer.id,
          duration: this.getFirstPlaylistSong.duration,
          title: this.getFirstPlaylistSong.title,
          link: this.getFirstPlaylistSong.link,
        };
        this.getWs.send(JSON.stringify(response));
      }
    },
    sendDislike() {},
    sendLike() {},
    addToPlaylist() {},
  },
  mounted() {
    console.log("user: " + this.getUser);
  },
};
</script>

<style>
.dj-table {
  width: 320px;
}

.green-thumb:hover {
  color: green !important;
}

.green-thumb {
  color: white !important;
}

.red-thumb:hover {
  color: crimson !important;
}

.red-thumb {
  color: white !important;
}

.blue-thumb:hover {
  color: rgb(46, 82, 225) !important;
}

.blue-thumb {
  color: white !important;
}
</style>