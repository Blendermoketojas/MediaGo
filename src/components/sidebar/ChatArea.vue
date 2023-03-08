<template>
    <div class="d-flex justify-content-center align-items-center chat-sizing bg-dark">
        <input v-model="message" @keydown.enter="sendMessage" class="input-style"
            placeholder="Type here to join the conversation" />
    </div>
</template>

<script>
export default {
    // emits: ['chatMessage'],
    methods: {
        sendMessage(event) {
            console.log("on enter" + this.user.name + " " + this.server.id)
            let type = "message";
            let text = this.message;
            if (!this.ws) {
                console.log("No WebSocket connection.");
                return;
            }
            if (true) // If user is an admin.
            {
                if (text.startsWith("/ban")) {
                    type = "ban";
                    text = text.substring(5);
                }
            }
            const response =
            {
                type: type,
                username: this.user.name,
                roomId: this.server.id,
                text: text
            };
            this.ws.send(JSON.stringify(response));
            this.message = '';
        },
    },
    computed: {
        ws() {
            return this.$store.getters.getWs;
        },
        user() {
            return this.$store.getters.getUser;
        },
        server() {
            return this.$store.getters.getSelectedServer;
        }
    },
    data() {
        return {
            message: ''
        }
    }
}
</script>

<style>
.chat-sizing {
    height: 65px;
    width: 380px;
}

.input-style {
    background-color: #282c35;
    color: white;
    width: 350px;
    height: 40px;
    border-radius: 10px;
}
</style>