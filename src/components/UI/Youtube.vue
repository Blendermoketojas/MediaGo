<template>
  <YouTube
    class="glowing-circle video-container"
    :videoid="observedInitData?.queue[0]?.link"
    :vars="{ autoplay: 1, controls: 0, fs: 0 }"
    :src="videoUrl"
    @state-change="onPlayerStateChange"
    autoplay="1"
    @ended="videoEnded"
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
    };
  },
  methods: {
    onPlayerReady() {
      this.$refs.youtube.playVideo();
      this.$store.commit(
        "setVideoDuration",
        Math.round(this.$refs.youtube.getDuration())
      );
      this.getVideoTitle();
      console.log("onReady ran");
    },

    onPlayerStateChange(event) {
      console.log("onPlayerStateChange() ran");
      switch (event.data) {
        case YT.PlayerState.PLAYING:
          this.onPlayerReady();
          this.isPlaying = setInterval(this.updateCurrentTime, 1000);
          break;
        case YT.PlayerState.ENDED:
          clearInterval(this.isPlaying);
          this.$store.commit("setCurrentVideoPlayTime", 0);
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
    getVideoTitle() {
      this.$http
        .get("https://www.googleapis.com/youtube/v3/videos", {
          params: {
            part: "snippet",
            id: this.videoId,
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
    observedInitData() {
      return this.getInitializationData;
    },
  },
  watch: {
    deep: true,
  },
  mounted() {
    eventBus.on("queueChange", (eventData) => {
      this.videoId = eventData?.queue[0]?.link.match(/(?<=v=)[\w-]+/)[0];
      this.$refs.youtube.pauseVideo(); // Pause the current video
      this.$refs.youtube.loadVideoById({
        videoId: this.videoId,
        startSeconds: eventData?.timer,
      });
      this.$refs.youtube.playVideo(); // Play the loaded video
      this.$refs.youtube.$emit("state-change", {
        data: YT.PlayerState.PLAYING,
      });
    });
  },
  unmounted() {
    clearInterval(this.isPlaying);
  },
};
</script>

<style>
.glowing-circle {
  box-shadow: 0 0 10px 5px #b400ff;
}
</style>