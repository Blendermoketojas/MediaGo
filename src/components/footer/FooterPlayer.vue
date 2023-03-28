<template>
  <div
    class="d-flex w-100 footer-position bg-dark align-items-center text-white"
    style="height: 83px"
  >
    <div>
      <font-awesome-icon
        class="me-5"
        icon="fa-solid fa-compact-disc"
        style="font-size: 50px; color: #828282"
      />
    </div>
    <div class="section-margin">
      <button @click="toggleDialog" class="d-flex flex-column">
        <span class="d-block">My first playlist</span>
        <span style="color: #828282">Add a song to play</span>
      </button>
    </div>
    <div class="vl"></div>
    <div class="d-flex flex-column ms-5 mb-2" style="min-width: 600px">
      <div class="mb-3">
        <span
          >{{ djName }} <span style="color: #828282">is playing</span>
          {{ this.$store.getters.getVideoTitle }}
        </span>
      </div>
      <div>
        <v-progress-linear :color='getServer?.theme?.color' :model-value="videoProgress">
          <v-tooltip activator="parent" location="start"
            >Tooltip</v-tooltip
          ></v-progress-linear
        >
      </div>
    </div>
    <span class="mt-5 ms-1">{{ videoDuration }}</span>
  </div>
</template>
<script>
import eventBus from "../../EventBus";

export default {
  data() {
    return {
      djName: "",
    };
  },
  methods: {
    toggleDialog() {
      this.$store.commit("setCreationModalIs", "playlist");
      this.$store.commit("toggleShowPlaylistDialog");
    },
  },
  computed: {
    videoDuration() {
      const videoDuration = this.$store.getters.getVideoDuration;
      const seconds = videoDuration % 60;
      const minutes = Math.floor(videoDuration / 60);
      return `${minutes}:${seconds}`;
    },
    videoProgress() {
      return (
        (this.$store.getters.getCurrentVideoPlayTime /
          this.$store.getters.getVideoDuration) *
        100
      );
    },
    getServer() {
      return this.$store.getters.getSelectedServer;
    }
  },
  mounted() {
    eventBus.on("queueChange", (eventData) => {
      this.djName = eventData?.queue[0]?.username;
    });
  },
};
</script>

<style>
.footer-position {
  background-color: red;
}

.vl {
  border-left: 1px solid #828282;
  height: 50px;
}

.section-margin {
  margin-right: 5rem;
}
</style>