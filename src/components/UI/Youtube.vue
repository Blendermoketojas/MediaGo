<template>
    <YouTube class="glowing-circle video-container" :videoid="video_id" :vars="{ 'autoplay': 1, 'controls': 0, 'fs': 0 }" :src="videoUrl"
        @state-change="onPlayerStateChange" autoplay="1" @ready="onPlayerReady" @ended="videoEnded" ref="youtube" />
</template>

<script>
import YouTube from 'vue3-youtube'

export default {
    components: { YouTube },
    data() {
        return {
            videoId: ' ',
            isPlaying: null,
        }
    },
    props: {
        videoUrl: {
            type: String,
            required: true
        }
    },
    methods: {
        onPlayerReady() {
            this.$refs.youtube.playVideo()
            this.$store.commit('setVideoDuration', this.$refs.youtube.getDuration())
            this.getVideoTitle();
            console.log("onReady ran")
        },
        onPlayerStateChange(event) {
            switch(event.data) {
                case YT.PlayerState.PLAYING:
                this.isPlaying = setInterval(this.updateCurrentTime, 1000);
                break;
                case YT.PlayerState.ENDED:
                clearInterval(this.isPlaying);
                this.$store.commit('setCurrentVideoPlayTime', 0);
                this.videoEnded();
                break;
            }  
        },
        updateCurrentTime() {
            this.$store.commit('setCurrentVideoPlayTime', Math.round(this.$refs.youtube.getCurrentTime()));
        },
        videoEnded() {
            clearInterval(this.isPlaying);
            this.$store.commit('setCurrentVideoPlayTime', 0);
        },
        getVideoTitle() {
            this.$http.get('https://www.googleapis.com/youtube/v3/videos', {
                params: {
                    part: 'snippet',
                    id: this.videoId,
                    key: this.$store.getters.getYT_API_KEY,
                },
            }).then((response) => {
                this.$store.commit('setVideoTitle', response.data.items[0].snippet.title);
            })
            .catch((error) => {
                console.error(error);
            });
        },
    },
    mounted() {
        this.videoId = this.videoUrl.match(/(?<=v=)[\w-]+/)[0];
        console.log(this.videoId);
    },
    unmounted() {
        console.log("UNMOUNTED IN YOUTUBE VUE")
        clearInterval(this.isPlaying);
    }
}
</script>

<style>
.glowing-circle {
  box-shadow: 0 0 10px 5px #b400ff;
}

</style>