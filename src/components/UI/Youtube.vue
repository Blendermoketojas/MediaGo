<template>
  <YouTube
    class="video-container"
    :style="{'box-shadow': `0 0 10px 5px ${getServer?.theme?.color}` }"
    :videoid="observedInitData?.queue[0]?.link"
    :vars="{ autoplay: 1, controls: 0, fs: 0 }"
    :src="videoUrl"
    @state-change="onPlayerStateChange"
    autoplay="1"
    @ended="videoEnded"
    @ready="onPlayerReady"
    ref="youtube"
  />
</template>

<script>
import YouTube from "vue3-youtube";
import { mapGetters } from "vuex";
import eventBus from "../../EventBus";

export default {
  components: { YouTube },
  data() {
    return {
      videoId: " ",
      isPlaying: null,
      nextSong: null,
      mountedPlayer: false,
      useJoinTimer: true,
      joinedTimer: 0,
      allowToPlayNext: false,
      justJoined: true,
    };
  },
  methods: {
    onPlayerReady() {
      this.mountedPlayer = true;
    },
    onPlayerStateChange(event) {
      switch (event.data) {
        case YT.PlayerState.PLAYING:
          this.$store.commit(
            "setVideoDuration",
            Math.round(this.$refs.youtube.getDuration())
          );
          this.getVideoTitle();
          this.isPlaying = setInterval(this.updateCurrentTime, 1000);
          break;
        case YT.PlayerState.ENDED:
          this.videoEnded();
          break;
      }
    },
    updateCurrentTime() {
      this.$store.commit(
        "setCurrentVideoPlayTime",
        Math.round(this.$refs.youtube.getCurrentTime())
      );
    },
    videoEnded() {
      clearInterval(this.isPlaying);
      this.$store.commit("setCurrentVideoPlayTime", 0);
    },
    loadAndPlay() {
      this.videoId = this.nextSong?.link.match(/(?<=v=)[\w-]+/)[0];
      let timer = 0;
      if (this.useJoinTimer) {
        timer = this.joinedTimer;
        this.useJoinTimer = false;
      }
      this.$refs.youtube.loadVideoById({
        videoId: this.videoId,
        startSeconds: timer,
      });
      console.log("starting video on: " + timer + " second");
      this.$store.commit(
        "setVideoDuration",
        Math.round(this.$refs.youtube.getDuration())
      );
      this.$refs.youtube.playVideo(); // Play the loaded video
    },
    getVideoTitle() {
      this.$http
        .get("https://www.googleapis.com/youtube/v3/videos", {
          params: {
            part: "snippet",
            id: this.nextSong?.link.match(/(?<=v=)[\w-]+/)[0],
            key: this.$store.getters.getYT_API_KEY,
          },
        })
        .then((response) => {
          this.$store.commit(
            "setVideoTitle",
            response?.data?.items[0]?.snippet?.title
          );
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  computed: {
    ...mapGetters(["getInitializationData"]),
    getServer() {
      return this.$store.getters.getSelectedServer;
    },
    observedInitData() {
      return this.getInitializationData;
    },
  },
  mounted() {
    eventBus.on("start-playing-song", (eventData) => {
      this.loadAndPlay();
    });
    eventBus.on("stop-playing-song", (eventData) => {
      this.$refs.youtube.stopVideo();
      this.$refs.youtube.$emit("state-change", { data: YT.PlayerState.ENDED });
    });
  },
  watch: {
    observedInitData: {
      handler(newVal, oldVal) {
        this.allowToPlayNext = !newVal.isPlaying;
        if (newVal.queue[0]) {
          this.nextSong = newVal.queue[0];
        } else {
          this.nextSong = null;
        }
        if (this.justJoined) {
          this.joinedTimer = newVal.elapsedTime;
          this.loadAndPlay();
          this.justJoined = false;
        }
      },
      deep: true,
    },
  },
  unmounted() {
    eventBus.off("queueChange");
    clearInterval(this.isPlaying);
  },
};
</script>

<style>
.glowing-circle {
  box-shadow: 0 0 10px 5px var(--default-theme);
}
</style>