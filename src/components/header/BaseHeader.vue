<template>
  <Teleport to="body">
    <v-dialog v-model="serverDescription" width="600">
      <v-card>
        <v-card-title>
          <span class="text-h5">About {{ getSelectedServer?.name }}</span>
        </v-card-title>
        <v-card-text>{{ getSelectedServer?.description }}</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="red-darken-1"
            variant="text"
            @click="serverDescription = false"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </Teleport>
  <header class="p-2 text-bg-dark">
    <div class="d-flex flex-row justify-content-between">
      <div class="d-flex align-items-center">
        <font-awesome-icon
          class="ms-2 display-6 custom-color"
          icon="fa-solid fa-headphones-simple"
        />
        <h2 class="d-inline ms-5">
          {{
            this.$store.getters?.getSelectedServer?.name || "No server selected"
          }}
        </h2>
        <div
          v-if="this.$store.getters.getSelectedServer"
          class="align-self-center ms-5"
        >
          <font-awesome-icon icon="fa-solid fa-eye" class="custom-color-eye" />
          <span class="fw-bold ms-2">{{ clientsCount }}</span>
          <v-tooltip activator="parent" location="bottom"
            ><span>People in this room right now</span></v-tooltip
          >
        </div>
        <div class="ms-5">
          <div v-if="this.$store.getters.getSelectedServer">
            <button
              @click="serverDescription = true"
              class="btn btn-outline-light"
            >
              <font-awesome-icon icon="fa-solid fa-info-circle" /> About
              community
              <v-tooltip activator="parent" location="bottom"
                >Click too see information about this <br />
                server like description, rules etc...</v-tooltip
              >
            </button>
            <button class="btn btn-outline-light ms-2">
              <font-awesome-icon icon="fa-solid fa-star" />
              <v-tooltip activator="parent" location="bottom"
                >Amount of people following this server</v-tooltip
              >
              {{ this.$store.getters?.getSelectedServer?.users }}
            </button>
            <button
              @click="openEditDialog"
              v-if="
                this.$store.getters?.getUser?.id ===
                this.$store.getters?.getSelectedServer?.owner
              "
              class="btn btn-outline-warning ms-2"
            >
              <v-tooltip activator="parent" location="bottom"
                >Only visible to the owner</v-tooltip
              >
              Edit server
            </button>
            <button @click="leaveServer" class="btn btn-outline-danger ms-2">
              <v-tooltip activator="parent" location="bottom"
                >Leave to waiting room</v-tooltip
              >
              <font-awesome-icon icon="fa-solid fa-right-from-bracket" />
            </button>
          </div>
        </div>
      </div>

      <div class="d-flex align-items-center">
        <base-avatar
          :username="this.$store.getters.getUser?.name"
        ></base-avatar>
      </div>
    </div>
  </header>
</template>

<script>
import BaseAvatar from "../UI/BaseAvatar.vue";
import eventBus from "../../EventBus";
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      clientsCount: 1,
      serverDescription: false,
    };
  },
  components: {
    BaseAvatar,
  },
  methods: {
    leaveServer() {
      this.$store.dispatch("leaveServer");
      this.$router.push({ path: "/floor/waiting_room" });
    },
    openEditDialog() {
      this.$store.commit("setIsEditingMode", true);
      this.$store.commit("setCreationModalIs", "server");
      eventBus.emit("open-server-edit");
    },
  },
  computed: {
    ...mapGetters(["getInitializationData", "getSelectedServer"]),
    observedInitData() {
      return this.getInitializationData;
    },
  },
  watch: {
    observedInitData: {
      handler(newVal, oldVal) {
        this.clientsCount = newVal.clientsCount;
      },
      deep: true,
    },
  },
  props: {
    // roomName: {
    //   type: String,
    //   required: true,
    //   default: "No room joined"
    // }
  },
};
</script>

<style scoped>
.custom-color {
  color: #474747;
}

.custom-color-eye {
  color: crimson;
}
</style>