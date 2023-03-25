<template>
  <Teleport to="body">
    <playlist-dialog>
    </playlist-dialog>
  </Teleport>
  <!-- <Teleport to="body">
    <dialog-loader>

    </dialog-loader>
  </Teleport> -->
  <keep-alive>
    <Teleport to="body"> <server-dialog>

      </server-dialog></Teleport>
  </keep-alive>

  <base-header></base-header>
  <div class="d-flex flex-row justify-content-between">
    <aside>
      <base-sidebar></base-sidebar>
    </aside>

    <div class="flex-fill">
      <div class="d-flex flex-column h-100">
        <main class="retro-background position-relative" style="min-height: calc(100vh - 150px);">
          <div class="d-flex justify-content-center mt-3">
            <youtube width="400px" height="200px"
              allowfullscreen="false" @ready="onReady" ref="youtube" />
          </div>
          <!-- <img :src="gifsArray.gif1" alt="GIF" class="stickman">
          <img :src="gifsArray.gif2" alt="GIF" class="stickman">
          <img :src="gifsArray.gif3" alt="GIF" class="stickman">
          <img :src="gifsArray.gif4" alt="GIF" class="stickman">
          <img :src="gifsArray.gif5" alt="GIF" class="stickman">
          <img :src="gifsArray.gif6" alt="GIF" class="stickman"> -->
          <div class="position-absolute bottom-0 start-50 translate-middle-x" style="margin-bottom: 10vh">
            <base-controls></base-controls>
          </div>
          <!-- <img :src="gifsArray.gif1" alt="GIF" class="stickman">
          <img :src="gifsArray.gif2" alt="GIF" class="stickman">
          <img :src="gifsArray.gif3" alt="GIF" class="stickman">
          <img :src="gifsArray.gif4" alt="GIF" class="stickman">
          <img :src="gifsArray.gif5" alt="GIF" class="stickman">
          <img :src="gifsArray.gif6" alt="GIF" class="stickman"> -->
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
import gif1 from "../assets/better gifs/2nd.gif";
import gif1back from "../assets/better gifs/2ndback.gif";
import gif2 from "../assets/better gifs/4th.gif";
import gif2back from "../assets/better gifs/4thback.gif";
import gif3 from "../assets/better gifs/5th.gif";
import gif3back from "../assets/better gifs/5thback.gif";
import gif4 from "../assets/better gifs/6th.gif";
import gif4back from "../assets/better gifs/6thback.gif";
import gif5 from "../assets/better gifs/7th.gif";
import gif5back from "../assets/better gifs/7thback.gif";
import gif6 from "../assets/better gifs/10.gif";
import gif6back from "../assets/better gifs/10back.gif";

import BaseHeader from "../components/header/BaseHeader.vue";
import BaseSidebar from "../components/sidebar/BaseSidebar.vue";
import BaseChat from "../components/sidebar/BaseChat.vue";
import FooterPlayer from "../components/footer/FooterPlayer.vue";
import Youtube from "../components/UI/Youtube.vue";
import ServerItem from "../components/UI/serverlist/ServerItem.vue";
import PlaylistDialog from "../components/UI/PlaylistDialog.vue";
import ServerDialog from "../components/UI/ServerDialog.vue";
import BaseControls from "../components/controlUI/BaseControls.vue";
import DialogLoader from "../components/UI/DialogLoader.vue";

export default {
  components: {
    BaseHeader,
    BaseSidebar,
    BaseChat,
    FooterPlayer,
    Youtube,
    ServerItem,
    ServerDialog,
    PlaylistDialog,
    BaseControls,
    DialogLoader
  },
  methods: {
    init(roomInfo) {
      if (this.ws) {
        this.ws.onerror = this.ws.onopen = this.ws.onclose = null;
        this.ws.close();
      }
      this.$store.commit('setWs', new WebSocket(`ws://${this.$store.getters.getFrontendIP}:6800`));
      this.ws.onopen = () => { this.ws.send(JSON.stringify(roomInfo)) };
      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'chat') this.addMessage(data.message) //showMessage(data.message); // Update chat for client.
        else if (data.type === "clientJoined") {
            this.$store.commit('setInitializationData', data);
        }
        else if (data.type === 'clientSizeUpdate') this.$store.commit('setInitializationData', data);
        else if (data.type === 'likeUpdate') {
          console.log("likes updated")
          // document.getElementById("allLikes").innerHTML = data.update; // Update likes for client.
          if (data.reset) console.log('reset') // switchLikeButtons(false);
        }
        else if (data.type === 'disconnect' && data.username === username) console.log("disconnect") // window.location.href = "../chat/createJoinRoom.html"; // Disconnect the client from the room.
        else if (data.type === 'queueUpdate') {
          this.$store.commit('setInitializationData', data);
        } // switchLikeButtons(data.isEmpty); // If queue is empty, disable like buttons.
        else if (data.type === 'banned' && data.username === username) // RENALDAS: userId negalejau padaryt cia, nes funkcija /ban [username] rasosi
        {

        }
        else if (data.type === 'skipped' && data.userId === userId) console.log("Your song has been skipped"); // RENALDAS: kai zmogaus daina buna praskipinta.
        else if (data.type === 'tookOutSong' && data.userId === userId) console.log("Song has been successfully taken out");
      }
      this.ws.onclose = () => { this.ws = null; }
    },
    addMessage(message) {
      this.$refs.chat.pushMessage(message);
    }
  },
  data() {
    return {
      user: null,
      gifsArray: {
        gif1: gif1,
        gif1back: gif1back,
        gif2: gif2,
        gif2back: gif2back,
        gif3: gif3,
        gif3back: gif3back,
        gif4: gif4,
        gif4back: gif4back,
        gif5: gif5,
        gif5back: gif5back,
        gif6: gif6,
        gif6back: gif6back,
      },
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
        if(!newVal) {
          this.ws.send('close')
          console.log("user leaves")
        }
        this.init({ roomId: newVal.id, type: "subscribe", username: this.user.name, userId: this.user.id })
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
  unmounted() {
    this.ws.send('close')
    console.log("user leaves")
  }
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
  background-image: url("../assets/pultas.png");
  background-repeat: no-repeat;
  background-size: contain;
  background-position: center center;
  background-size: 100% 100%;
  /* z-index: 0; */
}
</style>