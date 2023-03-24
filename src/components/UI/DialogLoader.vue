<template>
    <div class="text-center">
      <v-dialog
        v-model="dialog"
        :scrim="false"
        persistent
        width="auto"
      >
        <v-card
          color="primary"
        >
          <v-card-text>
            Please stand by
            <v-progress-linear
              indeterminate
              color="white"
              class="mb-0"
            ></v-progress-linear>
          </v-card-text>
        </v-card>
      </v-dialog>
    </div>
  </template>

<script>
  export default {
    data () {
      return {
        dialog: true,
      }
    },
    methods: {
        turnOnDialog() {
            this.dialog = true;
        },
        turnOffDialog() {
            this.dialog = false;
        }
    }
  }
</script>