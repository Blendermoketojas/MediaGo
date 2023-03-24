<template>
    <div class="text-center">
        <v-dialog v-model="isModalShown" z-index="1000" persistent width="1024">
            <v-card>
                <v-card>
                    <v-card-title>
                        <span class="text-h5">Create your server to begin the fun!</span>
                    </v-card-title>
                    <v-card-text>
                        <v-container>
                            <v-row>
                                <v-col cols="12" sm="6" md="6">
                                    <v-text-field v-model="formData.name" label="Server name*" required></v-text-field>
                                </v-col>
                                <v-col cols="12" sm="6" md="6">
                                    <v-autocomplete v-model="formData.genre" item-title="name" item-value="id"
                                        :items="this.$store.getters?.getAllGenres || [{ id: 0, name: 'fetching...' }]"
                                        label="Genre*"></v-autocomplete>
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <v-autocomplete v-model="formData.country" item-title="name" item-value="id"
                                        :items="this.$store.getters?.getAllCountries || [{ id: 0, name: 'fetching...' }]"
                                        label="Country*"></v-autocomplete>
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <v-autocomplete v-model="formData.theme" item-title="name" item-value="id"
                                        :items="[{ id: 1, name: 'default' }]" label="Themes*"></v-autocomplete>
                                </v-col>
                                <v-col cols="12" sm="12">
                                    <v-textarea v-model="formData.description" label="Description"></v-textarea>
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
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
import { reactive } from 'vue';
import eventBus from '../../EventBus';
import { hasListener } from '../../utils';

export default {

    data() {
        return {
            isShown: false,
            formData: reactive({
                name: "",
                owner: this.$store.getters?.getUser?.id,
                theme: "",
                genre: "",
                country: "",
                description: ""
            }),
        }
    },
    computed: {
        isModalShown() {
            return this.$store.getters.getIsCreationModalShown
        }
    },
    props: {
        creationMode: {
            type: String,
            required: true
        }
    },
    methods: {
        toggleIsShown() {
            this.$store.commit('toggleIsCreationModalShown');
            if (this.$store.getters.isEditingMode) {
                this.formData = reactive({ ...this.$store.getters.getSelectedServer })
            }
        },
        handleCreation() {
            // if (this.creationMode === "server") {
                this.$http({
                    method: "post",
                    url: `http://${this.$store.getters.getBackendIP}:5000/server_add`,
                    data: { ...this.formData },
                }).then((response) => this.$store.commit('addServer', response.data)).then((response) => this.isShown = false);
            // }
        },
    },
    mounted() {
        if (!hasListener(eventBus, 'open-server-edit')) {
            eventBus.on('open-server-edit', () => {
                // Do something here
                this.toggleIsShown();
            });
        }
    },
    beforeUnmount() {
        eventBus.off('open-server-edit', this.toggleIsShown);
    }
}
</script>

<style></style>