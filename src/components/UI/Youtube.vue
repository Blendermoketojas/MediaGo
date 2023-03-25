<template>
  <YouTube
    class="glowing-circle video-container"
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
      allowToPlayNext: false
    };
  },
  methods: {
    onPlayerReady() {
      console.log(this.$refs.youtube.getPlayerState())
      if (!this.mountedPlayer && this.nextSong) {
        this.loadAndPlay();
        this.$store.commit(
            "setVideoDuration",
            Math.round(this.$refs.youtube.getDuration())
          );
          this.getVideoTitle();
        console.log("onReady ran");
      }
      this.mountedPlayer = true;
    },
    onPlayerStateChange(event) {
      switch (event.data) {
        case YT.PlayerState.PLAYING:
          console.log("PLAYER STATE PLAYING");
          this.$store.commit(
            "setVideoDuration",
            Math.round(this.$refs.youtube.getDuration())
          );
          this.getVideoTitle();
          this.isPlaying = setInterval(this.updateCurrentTime, 1000);
          break;
        case YT.PlayerState.ENDED:
          console.log("PLAYER STATE ENDED");
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
      if(this.nextSong && this.allowToPlayNext) {
        this.loadAndPlay();
      }
    },
    loadAndPlay() {
      this.allowToPlayNext = false;
      this.videoId = this.nextSong?.link.match(/(?<=v=)[\w-]+/)[0];
      let timer = 0;
      if(this.useJoinTimer) {
        timer = this.joinedTimer;
        this.useJoinTimer = false;
      }
      this.$refs.youtube.loadVideoById({
        videoId: this.videoId,
        startSeconds: timer,
      });
      console.log("PLAY LAODED VIDEO");
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
    observedInitData() {
      console.log("init data changed in youtube player")
      return this.getInitializationData;
    },
  },
  mounted() {
    eventBus.on("queueChange", (eventData) => {
      this.nextSong = eventData?.queue[0];
      this.joinedTimer = eventData.elapsedTime;
    });
  },
  watch: {
    nextSong: {
      handler(newVal, oldVal) {
        if (newVal && this.$refs.youtube.getPlayerState() !== 1) {
          console.log(JSON.stringify(newVal))
          this.loadAndPlay();
        }
      },
      immediate: true,
    },
    observedInitData: {
      handler(newVal, oldVal) {
        this.allowToPlayNext = !newVal?.isSongPlaying;
      },
      deep: true
    }
  },
  unmounted() {
    eventBus.off("queueChange");
    clearInterval(this.isPlaying);
  },
};
</script>

<style>
.glowing-circle {
  box-shadow: 0 0 10px 5px #b400ff;
}
</style>