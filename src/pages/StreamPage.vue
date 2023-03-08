<template>
  <Teleport to="body">
    <playlist-dialog>
    </playlist-dialog>
  </Teleport>
  <Teleport to="body">
    <server-dialog v-model="this.$store.getters.getShowServersDialog">

    </server-dialog>
  </Teleport>
  <base-header></base-header>
  <div class="d-flex flex-row justify-content-between">
    <aside>
      <base-sidebar></base-sidebar>
    </aside>

    <div class="flex-fill">
      <div class="d-flex flex-column">
        <main class="retro-background">
          <div class="d-flex justify-content-center mt-3">
            <youtube video-url="https://www.youtube.com/watch?v=jNQXAC9IVRw" allowfullscreen="false" width="640"
              height="360" @ready="onReady" ref="youtube" />
          </div>
        </main>
        <div class="">
          <footer-player></footer-player>
        </div>
      </div>
    </div>
    <aside>
      <base-chat ref="chat"></base-chat>
    </aside>
  </div>
</template>

<script>
import BaseHeader from "../components/header/BaseHeader.vue";
import BaseSidebar from "../components/sidebar/BaseSidebar.vue";
import BaseChat from "../components/sidebar/BaseChat.vue";
import FooterPlayer from "../components/footer/FooterPlayer.vue";
import Youtube from "../components/UI/Youtube.vue";
import ServerItem from "../components/UI/serverlist/ServerItem.vue";
import PlaylistDialog from "../components/UI/PlaylistDialog.vue";
import ServerDialog from "../components/UI/ServerDialog.vue";

export default {
  components: {
    BaseHeader,
    BaseSidebar,
    BaseChat,
    FooterPlayer,
    Youtube,
    ServerItem,
    ServerDialog,
    PlaylistDialog
  },
  methods: {
    init(roomInfo) {
      if (this.ws) {
        this.ws.onerror = this.ws.onopen = this.ws.onclose = null;
        this.ws.close();
      }
      this.$store.commit('setWs', new WebSocket('ws://localhost:6800'));
      this.ws.onopen = () => { this.ws.send(roomInfo) };
      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'chat') { console.log("chat") }//showMessage(data.message); // Update chat for client.
        else if (data.type === 'likeUpdate') {
          document.getElementById("allLikes").innerHTML = data.update; // Update likes for client.
          if (data.reset) console.log('reset') // switchLikeButtons(false);
        }
        else if (data.type === 'disconnect' && data.username === username) console.log("disconnect") // window.location.href = "../chat/createJoinRoom.html"; // Disconnect the client from the room.
        else if (data.type === 'queueUpdate') console.log("queueUpdate") // switchLikeButtons(data.isEmpty); // If queue is empty, disable like buttons.
      }
      this.ws.onclose = () => { this.ws = null; }
    }
  },
  data() {
    return {
      user: null,
    }
  },
  computed: {
    watchServer() {
      return this.$store.getters.getSelectedServer;
    },
    ws() {
      return this.$store.getters.getWs;
    }
  },
  watch: {
    watchServer: {
      handler(newVal, oldVal) {
        this.init({ roomId: newVal.id, type: 'subscribe', username: this.user.name })
      },
      immediate: false
    }
  },
  mounted() {
    this.user = this.$store.getters.getUser;
    // const roomInfo = sessionStorage.getItem("roomInfo");
    // const contents = JSON.parse(roomInfo);
    // roomId = contents.roomId;
    // username = contents.username;
    // init(roomInfo);
  },
};
</script>

<style scoped>
main {
  height: calc(100vh - 145px);
  z-index: 0;
}

.container-fluid {
  padding: 0;
}

.yt-size {
  width: 37%;
}

.retro-background {
  background-image: url("../assets/resized.jpeg");
  /* z-index: 0; */
}
</style>