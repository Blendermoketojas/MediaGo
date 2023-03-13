<template>
    <div class="d-flex flex-column align-items-stretch flex-shrink-0 bg-dark fixed-right" style="width: 320px;">
        <div class="container-flex">
            <div class="row">
                <div class="col active-link">
                    <a href="/"
                        class="d-flex align-items-center justify-items-center flex-shrink-0 p-3 link-dark text-decoration-none border-bottom">
                        <span class="fs-5 fw-semibold text-white">Live Chat</span>
                    </a>
                </div>
                <div class="col">
                    <a href="/"
                        class="d-flex align-items-center justify-items-center flex-shrink-0 p-3 link-dark text-decoration-none border-bottom">
                        <span class="fs-5 fw-semibold text-white">Queue</span>
                    </a>
                </div>
            </div>
        </div>
        <div ref="chatContainer" class="list-group list-group-flush border-bottom scrollarea sidebar-height overflow-auto">
            <div class="m-4">
                <ul>
                    <span v-if="getServer == null" class="text-white">Connect to a server to start a conversation!</span>
                    <base-comment v-for="message in messages" :key="Math.random()" :name="message.username"
                        :comment="message.text" :time="message.time"></base-comment>
                </ul>
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
            this.messages.push({...message, time: currentTime})
            this.scrollToBottom();
        },
        scrollToBottom() {
            const container = this.$refs.chatContainer;
            container.scrollTop = container.scrollHeight;
        },
    },
    computed: {
        getServer() {
            return this.$store.getters.getSelectedServer;
        }
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

