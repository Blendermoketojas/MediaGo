<template>
  <div class="d-flex flex-column flex-shrink-0 bg-dark sidebar-height position-fixed" style="width: 8rem">
    <ul class="nav nav-pills nav-flush flex-column mb-auto text-center">
      <button @click="openCreationDialog" v-if="additionVisible" href="#"
        class="nav-link text-white py-3 border-bottom w-100" aria-current="page" title="">
        <font-awesome-icon icon="fa fa-plus"></font-awesome-icon>
      </button>
      <nav-item v-for="item in items" :key="item.id || item.name" :name="item.name"></nav-item>
    </ul>
  </div>
</template>

<script>
import NavItem from "./NavItem.vue";
import CreationModal from "../CreationModal.vue";
import eventBus from "../../../EventBus";

export default {
  components: {
    NavItem,
    CreationModal
  },
  data() {
    return {
      // Define a `openCreationDialog` function reference
      openEditDialog: this.openCreationDialog,
    };
  },
  methods: {
    openCreationDialog() {
      this.$store.commit('setIsEditingMode', false);
      eventBus.emit('open-server-edit');
    },
  },
  props: {
    items: {
      type: Array || Object,
      required: false
    },
    additionVisible: {
      type: Boolean,
      required: false
    }
  },
};
</script>

<style scoped>
.sidebar-height {
  height: calc(100vh - 64px);
  margin-top: 4rem;
}
</style>