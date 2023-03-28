<template>
  <div class="d-flex flex-row justify-content-center">
    <base-card class="border">
      <v-tooltip :disabled="!isDisabled" activator="parent" location="left"
        ><span>You're already in queue!</span></v-tooltip
      >
      <button
        :disabled="isDisabled"
        @click="addSongToQueue"
        type="button"
        class="btn blue-thumb"
      >
        <font-awesome-icon icon="fa fa-music"></font-awesome-icon> Join queue
      </button>
    </base-card>
    <div class="dj-table"></div>
    <div>
      <v-tooltip v-if="areActionsDisabled" activator="parent" location="top"
        >You can perform actions when the song is playing</v-tooltip
      >
      <base-card
        class="d-flex flex-column justify-content-center align-items-center border"
        :class="{ 'pointer-none': areActionsDisabled }"
      >
        <div class="mb-4">
          <button
            :disabled="areActionsDisabled"
            type="button"
            class="fs-3 me-5 green-thumb"
            :class="{ 'disabled-actions': areActionsDisabled }"
            @click="
              () => {
                sendLikeDislike(true);
              }
            "
          >
            <font-awesome-icon icon="fa fa-thumbs-up"></font-awesome-icon>
          </button>
          <button
            :disabled="areActionsDisabled"
            type="button"
            class="fs-3 me-5 red-thumb"
            :class="{ 'disabled-actions': areActionsDisabled }"
            @click="
              () => {
                sendLikeDislike(false);
              }
            "
          >
            <font-awesome-icon icon="fa fa-thumbs-down"></font-awesome-icon>
          </button>
          <button
            :disabled="areActionsDisabled"
            type="button"
            class="fs-3 blue-thumb"
            :class="{ 'disabled-actions': areActionsDisabled }"
          >
            <font-awesome-icon icon="fa fa-plus"></font-awesome-icon>
          </button>
        </div>
        <v-progress-linear
          class="me-4"
          style="width: 90%; background-color: crimson"
          color="green"
          :model-value="progressBarValue"
        ></v-progress-linear>
      </base-card>
    </div>
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
      "getInitializationData",
    ]),
    observedInitData() {
      return this.getInitializationData;
    },
  },
  watch: {
    observedInitData: {
      handler(newVal, oldVal) {
        this.isDisabled = newVal.isDisabledButton;
        this.areActionsDisabled = !newVal.isPlaying;
        this.votedUsers = newVal.update?.votedUsers;
        console.log("updating like amount");
        this.likes = newVal.update.likeAmount;
        // Update the progress bar value
        this.progressBarValue = (100 / this.votedUsers?.length) * this.likes;
      },
      deep: true,
    },
  },
  data() {
    return {
      isDisabled: false,
      areActionsDisabled: false,
      clickedAction: false,
      votedUsers: 0,
      likes: 0,
      progressBarValue: 0,
      totalVotes: 0,
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
    sendLikeDislike(type) {
      const response = {
        type: "likeInput",
        userId: this.getUser.id,
        roomId: this.getSelectedServer.id,
        likeType: type,
        sentMoreThanOnce: this.clickedAction,
      };
      this.getWs.send(JSON.stringify(response));
    },
    addToPlaylist() {},
  },
  mounted() {},
};
</script>

<style>
.dj-table {
  width: 320px;
}

.disabled-actions {
  cursor: not-allowed;
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