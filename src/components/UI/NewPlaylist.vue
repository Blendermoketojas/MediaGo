<template>
  <Teleport to="body">
    <v-row justify="center">
      <v-dialog v-model="songDialog" persistent width="512">
        <v-card>
          <v-card-title>
            <span class="text-h5">Add a song</span>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <v-col cols="12" sm="12" md="12">
                  <v-text-field
                    label="Youtube link*"
                    required
                    v-model="form.link"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-container>
            <small>*indicates required field</small>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="blue-darken-1"
              variant="text"
              @click="songDialog = false"
            >
              Close
            </v-btn>
            <v-btn
              color="blue-darken-1"
              variant="text"
              @click="addSong"
            >
              Save
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
  </Teleport>
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
        <v-btn @click="toggleDialog" class="bg-dark text-white"
          ><font-awesome-icon icon="fa fa-plus"></font-awesome-icon
        ></v-btn>
        <v-btn class="bg-dark text-white" style="border-radius: 0 !important"
          ><font-awesome-icon icon="fa fa-trash"></font-awesome-icon
        ></v-btn>
      </v-btn-toggle>
    </div>
  </div>
</template>

<script>
import { reactive } from "vue";

export default {
  methods: {
    toggleDialog() {
      this.songDialog = !this.songDialog;
    },
    addSong() {
      this.$http({
        method: "post",
        url: `http://${this.$store.getters.getBackendIP}:5000/song_add`,
        data: { ...this.form },
      })
        .then((response) =>console.log(response.data))
        .then((response) => (this.songDialog = false));
    },
  },
  data() {
    return {
      songDialog: false,
      form: reactive({
        id: this.$store.getters?.getSelectedPlaylist.id,
        user_id: this.$store.getters?.getUser?.id,
        link: "",
      }),
    };
  },
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