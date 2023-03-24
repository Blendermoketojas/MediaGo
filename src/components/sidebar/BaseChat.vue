<template>
    <div class="d-flex flex-column align-items-stretch flex-shrink-0 bg-dark fixed-right" style="width: 320px;">
        <div class="container-flex">
            <div class="row">
                <div class="col" :class="{ 'active-link': selectedWindow === 'chat' }">
                    <button @click="toggleChat"
                        class="d-flex align-items-center justify-items-center flex-shrink-0 p-3 link-dark text-decoration-none border-bottom">
                        <span class="fs-5 fw-semibold text-white">Live Chat</span>
                    </button>
                </div>
                <div class="col" :class="{ 'active-link': selectedWindow === 'queue' }">
                    <button @click="toggleQueue"
                        class="d-flex align-items-center justify-items-center flex-shrink-0 p-3 link-dark text-decoration-none border-bottom">
                        <span class="fs-5 fw-semibold text-white">Queue</span>
                    </button>
                </div>
            </div>
        </div>
        <div @scroll="onScroll" ref="chatContainer"
            class="list-group list-group-flush border-bottom scrollarea sidebar-height overflow-auto">
            <div :class="{ 'm-4': selectedWindow === 'chat' }">
                <ul v-show="selectedWindow === 'chat'">
                    <span v-if="getServer == null" class="text-white">Connect to a server to start a conversation!</span>
                    <base-comment v-if="getServer" class="fw-semibold" name="[Server]"
                        :comment="welcomeMessage"></base-comment>
                    <base-comment v-for="message in messages" :key="Math.random()" :name="message.username"
                        :comment="message.text" :time="message.time"></base-comment>
                </ul>
                <v-card bg- v-show="selectedWindow === 'queue'" style="width: 100%;">
                    <v-list :items="items"></v-list>
                </v-card>
            </div>
        </div>
        <chat-area></chat-area>
    </div>
</template>

<script>
import ChatArea from './ChatArea.vue';
import BaseComment from './BaseComment.vue';

export default {
    components: {
        ChatArea,
        BaseComment
    },
    data() {
        return {
            messages: [],
            selectedWindow: 'chat',
            isScrolling: false,
            items: [
                {
                    title: 'Item #1',
                    value: 1,
                },
                {
                    title: 'Item #2',
                    value: 2,
                },
                {
                    title: 'Item #3',
                    value: 3,
                },
            ],
        }
    },
    methods: {
        calcCurrentTime() {
            const now = new Date();
            const hours = now.getHours()
            const minutes = now.getMinutes();
            return `${hours}:${minutes}`;
        },
        pushMessage(message) {
            const currentTime = this.calcCurrentTime();
            if(this.messages.length > 50) {
                this.messages.shift();
            }
            this.messages.push({ ...message, time: currentTime })
            if (!this.isScrolling && !this.isAtBottom()) {
                this.scrollToBottom();
            }
        },
        scrollToBottom() {
            const container = this.$refs.chatContainer;
            container.scrollTop = container.scrollHeight+10;
        },
        toggleChat() {
            console.log("toggle chat")
            this.selectedWindow = 'chat';
        },
        toggleQueue() {
            console.log("toggle queue")
            this.selectedWindow = 'queue';
        },
        onScroll() {
            this.isScrolling = !this.isAtBottom();
        },
        isAtBottom() {
            const container = this.$refs.chatContainer;
            const distanceFromBottom = container.scrollHeight - container.scrollTop - container.clientHeight;
            return distanceFromBottom <= 25;
        },
    },
    computed: {
        getServer() {
            return this.$store.getters.getSelectedServer;
        },
        welcomeMessage() {
            return `Welcome to the ${this.getServer?.name} chat!`
        },
    },
    watch: {
        getServer: {
            handler(newVal, oldVal) {
                this.messages = [];
            }
        }
    }
}
</script>

<style scoped>
.col {
    padding: 0;
    margin: 0;
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

