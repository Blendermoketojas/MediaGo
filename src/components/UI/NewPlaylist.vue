<template>
  <div
    class="d-flex flex-row custom-color justify-content-between"
    style="margin-top: 4rem; height: 3.5rem"
  >
    <div class="d-flex align-items-center">
      <span class="ms-5 custom-font text-white">{{ playlistName }}</span>
    </div>
    <div class="d-flex flex-column">
      <v-btn-toggle
        color="#373b3e"
        class="align-items-stretch h-100"
        v-model="toggle"
        divided
      >
        <v-btn class="bg-dark text-white"
          ><font-awesome-icon icon="fa fa-pencil"></font-awesome-icon
        ></v-btn>
        <v-btn class="bg-dark text-white"
          ><font-awesome-icon icon="fa fa-shuffle"></font-awesome-icon
        ></v-btn>
        <v-btn class="bg-dark text-white" style="border-radius: 0 !important;"
          ><font-awesome-icon icon="fa fa-trash"></font-awesome-icon
        ></v-btn>
      </v-btn-toggle>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    playlistName: {
      type: String,
      required: true,
      default: "first playlist",
    },
  },
};
</script>


<style scoped>
.custom-color {
  background-color: #4d5154;
}
.custom-font {
  font-size: 2rem;
  font-weight: 700;
}
</style>