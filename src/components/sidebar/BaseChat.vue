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
        <div class="list-group list-group-flush border-bottom scrollarea sidebar-height">
            <div class="m-4">
                <ul>
                    <base-comment name="Tadas" comment="labadiena" time="1:35PM"></base-comment>
                    <base-comment name="Jevgenij" comment="Sveiki" time="1:36PM"></base-comment>
                    <base-comment name="Renaldas" comment="heloo" time="1:37PM"></base-comment>
                    <base-comment name="Lukas L" comment="kas cia per daina" time="1:37PM"></base-comment>
                    <base-comment name="Lukas T" comment="labas rytas" time="1:38PM"></base-comment>
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

