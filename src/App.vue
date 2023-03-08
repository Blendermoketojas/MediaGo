<template>
  <router-view></router-view>
</template>

<script>
import StreamPage from './pages/StreamPage.vue';
import FrontPage from './pages/FrontPage.vue';

export default {
  name: 'App',
  components: {
    StreamPage,
    FrontPage
  }
}
</script>

<style>
/* iframe {
  pointer-events: none;
} */

/* width */
::-webkit-scrollbar {
  width: 10px;
}

/* Track */
::-webkit-scrollbar-track {
  background: #7a7c7f;
}

/* Handle */
::-webkit-scrollbar-thumb {
  background: #373b3e;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>
