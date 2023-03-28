<template>
  <div class="player-avatar">
    <img :src="avatar" :alt="playerName" />
    <div class="player-name">{{ username }}</div>
  </div>
</template>
  
  <script>
export default {
  props: {
    avatar: {
      type: String,
      required: true,
    },
    username: {
      type: String,
      required: true,
    },
  },
};
</script>
  
  <style scoped>
.player-avatar {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  margin: 1rem;
}
.player-name {
  margin-top: 0.5rem;
}
</style>