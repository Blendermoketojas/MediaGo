<template>
  <v-row justify="center">
    <v-dialog v-model="this.$store.getters.getShowServersDialog" fullscreen :scrim="false"
      transition="dialog-bottom-transition">
      <v-card color="#373b3e">
        <v-toolbar dark color="#212529" class="position-fixed">
          <v-toolbar-title><span style="color: white">
              <font-awesome-icon icon="fa-solid fa-people-group" /> Server explorer</span></v-toolbar-title>
          <v-spacer></v-spacer>
          <v-toolbar-items>
            <v-btn variant="text" color="white" @click="toggleDialog">
              Close
            </v-btn>
          </v-toolbar-items>
        </v-toolbar>
        <div class="d-flex">
          <keep-alive>
            <dialog-sidebar :items="navItems" :additionVisible="true"></dialog-sidebar>
          </keep-alive>
          <ul class="w-100">
            <server-menu @fetchServers="fetchServers"></server-menu>
            <server-item @turnOffDialog="toggleDialog" v-for="server in servers" :key="server.id" :id="server.id"
              :serverTitle="server.name" :genre="server.genre" :country="server.country" :users="server.users"
              :theme="server.theme"></server-item>
            <span v-if="servers?.length === 0" class="display-6 text-white m-3 fw-semibold">No servers found.</span>
          </ul>
        </div>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import DialogSidebar from "./playlist_dialog_components/DialogSidebar.vue";
import ServerItem from "./serverlist/ServerItem.vue";
import ServerMenu from "./ServerMenu.vue";

export default {
  components: {
    DialogSidebar,
    ServerItem,
    ServerMenu
  },
  data() {
    return {
      navItems: [{ id: 1, name: "Explore communities" }, { id: 2, name: 'Your likes' }],
      // HARDCODED FOR TEST PORPUSES
      // servers: [{ id: "65465161", name: "Disco server", theme: "#4894c6", country: 'France', genre: "Disco" },
      // { id: "15115615", name: "Dubstep lovers", theme: "#6548ds", country: 'Germany', genre: "Dubstep" }],
    };
  },
  computed: {
    servers() {
      return this.$store.getters.getServers;
    }
  },
  methods: {
    toggleDialog() {
      this.$store.commit('toggleShowServersDialog')
    },
    fetchServers() {

    }
  },
  mounted() {

  },
  created() {
    console.log("server dialog created")
  }
};
</script>

<style scoped>
ul {
  padding: 0;
  margin-left: 8rem;
}
</style>