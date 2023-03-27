<template>
    <div class="d-flex flex-column flex-shrink-0 bg-dark sidebar-height" style="width: 3rem;">
        <a href="/" class="d-block p-3 link-dark text-decoration-none">
            <svg class="bi" width="40" height="32">
                <use xlink:href="#bootstrap"></use>
            </svg>
            <span class="visually-hidden">Icon-only</span>
        </a>
        <ul class="nav nav-pills nav-flush flex-column mb-auto text-center">
            <li class="nav-item">
                <a href="#" class="nav-link active py-3 border-bottom" aria-current="page" title="" data-bs-toggle="tooltip"
                    data-bs-placement="right" data-bs-original-title="Home">
                    <font-awesome-icon icon="fa-solid fa-music" />
                </a>
            </li>
            <li>
                <button @click="toggleDialog" class="w-100 nav-link py-3 border-bottom text-white" title="" data-bs-toggle="tooltip"
                    data-bs-placement="right" data-bs-original-title="Dashboard">
                    <font-awesome-icon icon="fa-solid fa-people-group" />
                </button>
            </li>
            <li>
                <a href="#" class="nav-link py-3 border-bottom text-white" title="" data-bs-toggle="tooltip"
                    data-bs-placement="right" data-bs-original-title="Orders">
                    <font-awesome-icon icon="fa-solid fa-gear" />
                </a>
            </li>
        </ul>
    </div>
</template>

<script>
import {
    mdiPlaylistMusic
} from '@mdi/js'
export default {
    data() {
        return {
            icons: {
                mdiPlaylistMusic
            }
        }
    },
    methods: {
        toggleDialog() {
            this.$store.commit('setCreationModalIs', 'server');
            this.$store.commit('toggleShowServersDialog');
        },
    }
}
</script>

<style scoped>
.sidebar-height {
    height: calc(100vh - 62px);
}
</style>