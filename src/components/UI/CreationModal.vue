<template>
  <div class="text-center">
    <v-dialog v-model="isShown" z-index="1000" persistent :width="sizing.width">
      <v-card>
        <v-card-title>
          <span v-if="this.$store.getters.getIsEditingMode" class="text-h5"
            >Edit {{ creationMode }}</span
          >
          <span v-else-if="creationMode === 'server'" class="text-h5"
            >Create your server to begin the fun!</span
          >
          <span v-else-if="creationMode === 'playlist'" class="text-h5"
            >Create a playlist</span
          >
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row v-if="creationMode === 'server'">
              <v-col cols="12" sm="6" md="6">
                <v-text-field
                  v-model="formServer.name"
                  label="Server name*"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="6">
                <v-autocomplete
                  v-model="formServer.genre"
                  item-title="name"
                  item-value="id"
                  :items="
                    this.$store.getters?.getAllGenres || [
                      { id: 0, name: 'fetching...' },
                    ]
                  "
                  label="Genre*"
                ></v-autocomplete>
              </v-col>
              <v-col cols="12" sm="6">
                <v-autocomplete
                  v-model="formServer.country"
                  item-title="name"
                  item-value="id"
                  :items="
                    this.$store.getters?.getAllCountries || [
                      { id: 0, name: 'fetching...' },
                    ]
                  "
                  label="Country*"
                ></v-autocomplete>
              </v-col>
              <v-col cols="12" sm="6">
                <v-autocomplete
                  v-model="formServer.theme"
                  item-title="name"
                  item-value="id"
                  :items="
                    this.$store.getters?.getAllThemes || [
                      { id: 0, name: 'fetching...' },
                    ]
                  "
                  label="Themes*"
                ></v-autocomplete>
              </v-col>
              <v-col cols="12" sm="12">
                <v-textarea
                  v-model="formServer.description"
                  label="Description"
                ></v-textarea>
              </v-col>
            </v-row>
            <v-row v-else>
              <v-col cols="12" sm="12" md="12">
                <v-text-field
                  v-model="formPlaylist.name"
                  label="Playlist name*"
                  required
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
          <small>*indicates required field</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue-darken-1" variant="text" @click="toggleIsShown">
            Close
          </v-btn>
          <v-btn color="green" variant="text" @click="handleCreation">
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { reactive } from "vue";
import eventBus from "../../EventBus";
import { hasListener } from "../../utils";
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      creationMode: "",
      isShown: false,
      sizing: { width: "" },
      formServer: reactive({
        name: "",
        owner: this.$store.getters?.getUser?.id,
        theme: "",
        genre: "",
        country: "",
        description: "",
      }),
      formPlaylist: reactive({
        name: "",
      }),
    };
  },
  methods: {
    toggleIsShown() {
      this.creationMode = this.$store.getters.getCreationModalIs;
      if (this.creationMode === "server") {
        this.sizing.width = 1024;
        if (
          !this.$store.getters.getAllCountries ||
          !this.$store.getters.getAllGenres ||
          !this.$store.getters.getAllThemes
        ) {
          this.$store.dispatch("setAllGenres");
          this.$store.dispatch("setAllCountries");
          this.$store.dispatch("setAllThemes");
        }
        if (this.$store.getters.getIsEditingMode) {
          this.formServer = reactive({
            ...this.$store.getters.getSelectedServer,
          });
        } else {
          this.formServer = reactive({
            name: "",
            owner: this.$store.getters?.getUser?.id,
            theme: "",
            genre: "",
            country: "",
            description: "",
          });
        }
      } else {
        this.sizing.width = 512;
      }
      this.isShown = !this.isShown;
    },
    handleCreation() {
      if (this.$store.getters.getCreationModalIs === "server") {
        this.$http({
          method: "post",
          url: `http://${this.$store.getters.getBackendIP}:5000/${this.serverActions}`,
          data: { ...this.formServer },
        })
          .then((response) => this.$store.commit("addServer", response.data))
          .then((response) => (this.isShown = false));
      } else {
        this.$http({
          method: "post",
          url: `http://${this.$store.getters.getBackendIP}:5000/playlist_add`,
          data: { ...this.formPlaylist },
        })
          .then((response) => this.$store.commit("addPlaylist", response.data))
          .then((response) => (this.isShown = false));
      }
    },
  },
  computed: {
    ...mapGetters(["getIsEditingMode"]),
    playlistAction() {
      return this.getIsEditingMode ? "playlist_edit" : "playlist_add";
    },
    serverActions() {
      return this.getIsEditingMode ? "server_edit_info" : "server_add";
    },
  },
  mounted() {
    if (!hasListener(eventBus, "open-server-edit")) {
      eventBus.on("open-server-edit", () => {
        console.log("toggle shown");
        this.toggleIsShown();
      });
    }
  },
  beforeUnmount() {
    eventBus.off("open-server-edit", this.toggleIsShown);
  },
};
</script>

<style>
.custom-dialog {
  background-color: #212529;
  color: white;
}

.custom-dialog input,
.custom-dialog textarea,
.custom-dialog .v-select__slot {
  color: #373b3e;
  background-color: white;
}
</style>