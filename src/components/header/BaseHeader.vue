<template>
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
            <button class="btn btn-outline-light">
              <font-awesome-icon icon="fa-solid fa-info-circle" /> About
              community
            </button>
            <button class="btn btn-outline-light ms-2">
              <font-awesome-icon icon="fa-solid fa-star" />
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
              Edit server
            </button>
            <button @click="leaveServer" class="btn btn-outline-danger ms-2">
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
      eventBus.emit("open-server-edit");
    },
  },
  computed: {
    ...mapGetters(["getInitializationData"]),
    observedInitData() {
      console.log("init data changed in youtube player");
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