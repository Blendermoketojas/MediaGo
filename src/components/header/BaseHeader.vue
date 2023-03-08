<template>
  <header class="p-2 text-bg-dark">
    <div class="d-flex flex-row justify-content-between">
      <div class="d-flex align-items-center">
        <font-awesome-icon class="ms-2 display-6 custom-color" icon="fa-solid fa-headphones-simple" />
        <h2 class="d-inline ms-5">{{ this.$store.getters?.getSelectedServer?.serverTitle || "No server selected" }}</h2>
        <div class="align-self-center ms-5">
          <font-awesome-icon icon="fa-solid fa-eye" class="custom-color-eye " />
          <span class="fw-bold ms-2">3000</span>
        </div>
        <div class="ms-5">
          <button class="btn btn-outline-light"><font-awesome-icon icon="fa-solid fa-info-circle" /> About community</button>
          <button class="btn btn-outline-light ms-2"><font-awesome-icon icon="fa-solid fa-star" /> 1.3k</button>
        </div>
      </div>

      <div class="d-flex align-items-center">
        <router-link to="/authentication" class="btn btn-outline-light me-2">Login</router-link>
        <router-link to="/authentication" class="btn btn-warning">Sign-up</router-link>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  props: {
    // roomName: {
    //   type: String,
    //   required: true,
    //   default: "No room joined"
    // }
  }
}

</script>

<style scoped>
.custom-color {
  color: #474747;
}

.custom-color-eye {
  color: crimson;
}
</style>