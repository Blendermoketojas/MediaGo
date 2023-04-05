<template>
  <Teleport to="body">
    <playlist-dialog> </playlist-dialog>
  </Teleport>
  <!-- <Teleport to="body">
    <dialog-loader>

    </dialog-loader>
  </Teleport> -->
  <Teleport to="body">
    <creation-modal> </creation-modal>
  </Teleport>
  <keep-alive>
    <Teleport to="body"> <server-dialog> </server-dialog></Teleport>
  </keep-alive>

  <base-header></base-header>
  <div ref="streamWindow" class="d-flex flex-row justify-content-between">
    <aside>
      <base-sidebar></base-sidebar>
    </aside>

    <div class="flex-fill">
      <div class="d-flex flex-column h-100">
        <main
          class="position-relative"
          style="min-height: calc(100vh - 150px)"
          :style="retroBackgroundStyle"
          :class="{ 'retro-background': selectedServer === null }"
        >
          <div class="d-flex justify-content-center mt-3">
            <youtube
              width="400px"
              height="200px"
              allowfullscreen="false"
              @ready="onReady"
              ref="youtube"
            />
          </div>
          <div
            class="position-absolute bottom-0 start-50 translate-middle-x"
            style="margin-bottom: 10vh"
          >
            <base-controls v-if="selectedServer"></base-controls>
          </div>
          <!-- <v-container>
            <v-row no-gutters class="flex-row row-no-spacing">
              <v-col v-for="n in 20" :key="n" cols="1" class="col-no-spacing">
                <img :src="gifsArray.gif1" alt="GIF" class="stickman" />
              </v-col>
            </v-row>
          </v-container> -->
          <!-- <div id="app">
            <div class="avatars-container">
              <PlayerAvatar
                v-for="(player, index) in players"
                :key="index"
                :avatar="player.avatar"
                :playerName="player.name"
              />
            </div>
          </div> -->
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
import eventBus from "../EventBus";

import BaseHeader from "../components/header/BaseHeader.vue";
import BaseSidebar from "../components/sidebar/BaseSidebar.vue";
import BaseChat from "../components/sidebar/BaseChat.vue";
import FooterPlayer from "../components/footer/FooterPlayer.vue";
import Youtube from "../components/UI/Youtube.vue";
import ServerItem from "../components/UI/serverlist/ServerItem.vue";
import PlaylistDialog from "../components/UI/PlaylistDialog.vue";
import ServerDialog from "../components/UI/ServerDialog.vue";
import BaseControls from "../components/controlUI/BaseControls.vue";
// import PlayerAvatar from "../components/UI/DialogLoader.vue";
import DialogLoader from "../components/UI/DialogLoader.vue";
import CreationModal from "../components/UI/CreationModal.vue";
import { mapGetters } from "vuex";
import PlayerAvatar from "../components/UI/PlayerAvatar.vue";

const imageModules = import.meta.globEager("../assets/backgrounds/*.png");

const images = Object.entries(imageModules).reduce((acc, [path, module]) => {
  const filename = path.split("/").pop();
  acc[filename] = module.default;
  return acc;
}, {});

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
    DialogLoader,
    CreationModal,
    PlayerAvatar,
  },
  methods: {
    init(roomInfo) {
      if (this.ws) {
        this.ws.onerror = this.ws.onopen = this.ws.onclose = null;
        this.ws.close();
      }
      this.$store.commit(
        "setWs",
        new WebSocket(`ws://${this.$store.getters.getFrontendIP}:6800`)
      );
      this.ws.onopen = () => {
        this.ws.send(JSON.stringify(roomInfo));
      };
      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === "chat") this.addMessage(data.message);
        //showMessage(data.message); // Update chat for client.
        else if (data.type === "clientJoined") {
          this.$store.commit("setInitializationData", data);
        } else if (data.type === "clientSizeUpdate")
          this.$store.commit("setInitializationData", data);
        else if (data.type === "songStart") {
          this.$store.commit("setInitializationData", data);
          eventBus.emit("start-playing-song");
        } else if (data.type === "songEnd") {
          eventBus.emit("stop-playing-song");
          this.$store.commit("setInitializationData", data);
        } else if (data.type === "likeUpdate") {
          if (data.reset) {
            this.$store.commit("setInitializationData", {
              update: data.update,
            });
          } else {
            this.$store.commit("setInitializationData", data);
          }
        } else if (data.type === "disconnect" && data.username === username)
          console.log("disconnect");
        // window.location.href = "../chat/createJoinRoom.html"; // Disconnect the client from the room.
        else if (data.type === "queueUpdate") {
          this.$store.commit("setInitializationData", data);
        } // switchLikeButtons(data.isEmpty); // If queue is empty, disable like buttons.
        else if (data.type === "banned" && data.username === username) {
          // RENALDAS: userId negalejau padaryt cia, nes funkcija /ban [username] rasosi
        } else if (data.type === "skipped" && data.userId === userId)
          console.log("Your song has been skipped");
        // RENALDAS: kai zmogaus daina buna praskipinta.
        else if (data.type === "tookOutSong" && data.userId === userId)
          console.log("Song has been successfully taken out");
      };
      this.ws.onclose = () => {
        this.ws = null;
      };
    },
    addMessage(message) {
      this.$refs.chat.pushMessage(message);
    },
  },
  data() {
    return {
      user: null,
      players: [
        { name: 'Player 1', avatar: 'avatar1.png' },
        { name: 'Player 2', avatar: 'avatar2.png' },
        { name: 'Player 3', avatar: 'avatar3.png' }
      ],
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
    };
  },
  computed: {
    selectedServer() {
      return this.$store.getters.getSelectedServer;
    },
    ws() {
      return this.$store.getters.getWs;
    },
    retroBackgroundStyle() {
      const imageUrl = this.selectedServer?.theme?.link;
      const imageName = imageUrl?.replace("../assets/backgrounds/", "");
      const backgroundImageUrl = images[imageName];
      const defaultImageUrl = images["Cyber.png"];
      return {
        backgroundImage: `url("${backgroundImageUrl || defaultImageUrl}")`,
        backgroundRepeat: "no-repeat",
        backgroundSize: "contain",
        backgroundPosition: "center center",
        backgroundSize: "100% 100%",
      };
    },
  },
  watch: {
    selectedServer: {
      handler(newVal, oldVal) {
        console.log("getSelectedserver changed");
        if (newVal && this.ws) {
          this.ws.send(JSON.stringify({ type: "close" }));
        }
        this.init({
          roomId: newVal.id,
          type: "subscribe",
          username: this.user.name,
          userId: this.user.id,
        });
      },
      immediate: false,
      deep: true,
    },
  },
  mounted() {
    this.user = this.$store.getters.getUser;
    const streamWindow = this.$refs.streamWindow;
    streamWindow.addEventListener("wheel", (event) => {
      if (event.ctrlKey) {
        event.preventDefault();
      }
    });
    // const roomInfo = sessionStorage.getItem("roomInfo");
    // const contents = JSON.parse(roomInfo);
    // roomId = contents.roomId;
    // username = contents.username;
    // init(roomInfo);
  },
  unmounted() {
    // this.ws.send(JSON.stringify({ type: "close" }));
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

.row-no-spacing {
  margin-top: 4px;
  margin-bottom: -4px;
}

.col-no-spacing {
  padding-top: 10px;
  padding-bottom: 4px;
}

.yt-size {
  width: 37%;
}
.avatars-container {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 1rem;
  background-color: rgba(0, 0, 0, 0.5);
}

.retro-background {
  background-image: url("../assets/backgrounds/Cyber.png");
  background-repeat: no-repeat;
  background-size: contain;
  background-position: center center;
  background-size: 100% 100%;
  /* z-index: 0; */
}
</style>