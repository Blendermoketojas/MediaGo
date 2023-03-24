<template>
    <div class="d-flex justify-content-center align-items-center rounded-border-div">
        <slot>
            
        </slot>
    </div>
</template>
<script>
    export default {

    }
</script>

<style scoped>
    .rounded-border-div {
  height: 110px;
  width: 175px;
  border-radius: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  background-color: rgba(0, 0, 0, 0.5); /* Transparent background */
}

</style>