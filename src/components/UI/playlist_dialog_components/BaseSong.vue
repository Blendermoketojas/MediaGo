<template>
  <div
    class="d-flex justify-content-between align-items-center text-white hover-selection"
    style="height: 4rem"
  >
    <div class="">
      <img
        class="me-5 ms-5"
        :src=imgUrl
      />
      <span class="ms-3">{{ channelTitle }}</span>
    </div>
    <div class="">
      <span>{{ title }}</span>
    </div>
    <div class="pe-5">
      {{ duration }}
    </div>
  </div>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      required: true,
      default: "Kapitonas (Offical video)",
    },
    channelTitle: {
      type: String,
      required: true,
      default: "Rondo",
    },
    duration: {
      type: String,
      required: true,
      default: "3:26",
    },
    imgUrl: {
      type: String,
      required: true,
      default: "https://showmax.akamaized.net/i/12cdc789-bff1-47db-9f18-622c8565fa33/format=webp/q=70/850x"
    }
  },
};
</script>

<style scoped>
img {
  width: 70px;
}
.hover-selection:hover {
  background-color: #8f00ff;
  cursor: pointer;
}
</style>

<style>
.hover-selection:not(:last-child) {
    border-bottom: 1px solid white;
}
</style>