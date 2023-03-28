<template>
  <div
    class="d-flex flex-column align-items-stretch flex-shrink-0 bg-dark fixed-right"
    :class="{'pointer-none': !getServer}"
    style="width: 320px"
  >
    <div class="container-flex">
      <div class="row">
        <div
          class="col"
          :style="selectedWindow === 'chat' ? theme : null"
        >
          <button
            @click="toggleChat"
            class="d-flex align-items-center justify-items-center flex-shrink-0 p-3 link-dark text-decoration-none border-bottom"
          >
            <span class="fs-5 fw-semibold text-white">Live Chat</span>
          </button>
        </div>
        <div
          class="col"
          :style="selectedWindow === 'queue' ? theme : null"
        >
          <button
            @click="toggleQueue"
            class="d-flex align-items-center justify-items-center flex-shrink-0 p-3 link-dark text-decoration-none border-bottom"
          >
            <span class="fs-5 fw-semibold text-white">Queue</span>
          </button>
        </div>
      </div>
    </div>
    <div
      @scroll="onScroll"
      ref="chatContainer"
      class="list-group list-group-flush border-bottom scrollarea sidebar-height overflow-auto"
    >
      <div :class="{ 'm-4': selectedWindow === 'chat' }">
        <ul v-show="selectedWindow === 'chat'">
          <span v-if="getServer == null" class="text-white"
            >Connect to a server to start a conversation!</span
          >
          <base-comment
            v-if="getServer"
            class="fw-semibold"
            name="[Server]"
            :comment="welcomeMessage"
          ></base-comment>
          <base-comment
            v-for="message in messages"
            :key="message.username + Math.random()"
            :name="message.username"
            :comment="message.text"
            :time="message.time"
          ></base-comment>
        </ul>
        <v-card v-show="selectedWindow === 'queue'" style="width: 100%">
          <v-list
            bg-color="dark"
            class="playing"
            style="color: white"
            lines="one"
          >
            <v-list-item
              v-for="(data, index) in observedInitData"
              :key="data.title"
              :title="data.title"
              :subtitle="data.value"
            >
              <v-tooltip activator="parent" location="left">
                <div v-if="index === 0">
                  <span style="color: violet">This track is playing!</span>
                  <br />
                </div>
                <div v-if="index === 1">
                  <span style="color: yellow">Up next:</span>
                  <br />
                </div>
                {{ data.value }}</v-tooltip
              >
            </v-list-item>
          </v-list>
        </v-card>
      </div>
    </div>
    <chat-area></chat-area>
  </div>
</template>

<script>
import ChatArea from "./ChatArea.vue";
import BaseComment from "./BaseComment.vue";
import { mapGetters } from "vuex";
import eventBus from "../../EventBus";

export default {
  components: {
    ChatArea,
    BaseComment,
  },
  data() {
    return {
      messages: [],
      selectedWindow: "chat",
      isScrolling: false,
    };
  },
  methods: {
    calcCurrentTime() {
      const now = new Date();
      const hours = now.getHours();
      const minutes = now.getMinutes();
      const formattedMinutes = minutes < 10 ? `0${minutes}` : minutes;
      return `${hours}:${formattedMinutes}`;
    },
    pushMessage(message) {
      const currentTime = this.calcCurrentTime();
      if (this.messages.length > 50) {
        this.messages.shift();
      }
      this.messages.push({ ...message, time: currentTime });
      if (!this.isScrolling && !this.isAtBottom()) {
        this.scrollToBottom();
      }
    },
    scrollToBottom() {
      const container = this.$refs.chatContainer;
      container.scrollTop = container.scrollHeight + 10;
    },
    toggleChat() {
      this.selectedWindow = "chat";
    },
    toggleQueue() {
      this.selectedWindow = "queue";
    },
    onScroll() {
      this.isScrolling = !this.isAtBottom();
    },
    isAtBottom() {
      const container = this.$refs.chatContainer;
      const distanceFromBottom =
        container.scrollHeight - container.scrollTop - container.clientHeight;
      return distanceFromBottom <= 25;
    },
  },
  computed: {
    getServer() {
      return this.$store.getters.getSelectedServer;
    },
    welcomeMessage() {
      return `Welcome to the ${this.getServer?.name} chat!`;
    },
    ...mapGetters(["getInitializationData"]),
    observedInitData() {
      eventBus.emit("queueChange", this.getInitializationData);
      return this.getInitializationData?.queue.map((q) => ({
        title: q.username,
        value: q.videoTitle,
      }));
    },
    theme() {
      return { backgroundColor: this.getServer?.theme?.color };
    }
  },
  watch: {
    getServer: {
      handler(newVal, oldVal) {
        this.messages = [];
      },
    },
    // observedInitData: {
    //   handler(newVal, oldVal) {
    //     console.log("observedInitData has changed:", newVal);
    //     this.items = newVal?.queue.map((q) => ({
    //       title: q.username,
    //       value: newVal.title,
    //     }));
    //   },
    //   immediate: true,
    //   deep: true,
    // },
  },
};
</script>

<style scoped>
.col {
  padding: 0;
  margin: 0;
}

.playing > .v-list-item:first-child {
  background-color: green;
}

.sidebar-height {
  height: calc(100vh - 190px);
}

ul {
  padding: 0;
}

.active-link {
  background-color: #0d6efd;
}
</style>

