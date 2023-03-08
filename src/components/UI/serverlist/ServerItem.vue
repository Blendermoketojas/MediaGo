<template>
    <router-link :to=link @click="setSelectedServer"
        class="d-flex justify-content-between align-items-center text-white hover-selection" style="height: 4rem">
        <div class="">
            <img class="me-5 ms-5" :src=imgUrl />
            <span class="ms-3">{{ serverTitle }}</span>
        </div>
        <div class="">
            <span>{{ genre }}</span>
        </div>
        <div class="pe-5">
            {{ country }}
        </div>
    </router-link>
</template>
  
<script>
export default {
    props: {
        id: {
            type: String,
            required: true
        },
        country: {
            type: String,
            required: true,
            default: "Lithuania",
        },
        serverTitle: {
            type: String,
            required: true,
            default: "KVK I17",
        },
        genre: {
            type: String,
            required: true,
            default: "Lietuviska estrada",
        },
        imgUrl: {
            type: String,
            required: true,
            default: "https://showmax.akamaized.net/i/12cdc789-bff1-47db-9f18-622c8565fa33/format=webp/q=70/850x"
        }
    },
    computed: {
        link() {
            return `/floor/${this.id}`
        }
    },
    methods: {
        setSelectedServer() {
            const { id, country, serverTitle, genre, imgUrl } = this;
            this.$store.commit('setSelectedServer', { id, country, serverTitle, genre, imgUrl })
        }
    }
};
</script>
  
<style scoped>
a {
    text-decoration: none;
}

img {
    width: 70px;
}

.hover-selection:hover {
    background-color: #8f00ff;
    cursor: pointer;
}
</style>
  