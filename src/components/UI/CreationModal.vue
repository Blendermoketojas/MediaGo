<template>
    <div class="text-center">
        <v-dialog z-index="1000" v-model="isShown" persistent width="1024">
            <v-card>
                <template v-slot:activator="{ props }">
                    <v-btn color="primary" v-bind="props">
                        Open Dialog
                    </v-btn>
                </template>
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
                                    <v-autocomplete v-model="formData.genre" :items="['POP', 'Dubstep', 'Rock', 'Rap']"
                                        label="Genre*"></v-autocomplete>
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <v-autocomplete v-model="formData.country"
                                        :items="['LITHUANIA', 'USA', 'ENGLAND', 'GERMANY', 'FRANCE']"
                                        label="Country*"></v-autocomplete>
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <v-autocomplete v-model="formData.theme"
                                        :items="['Default', 'Monstercat', 'Ice', 'Fire']" label="Themes*"></v-autocomplete>
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
                        <v-btn color="green" variant="text" @click="dialog = false">
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

export default {
    data() {
        return {
            isShown: false,
            formData: reactive({
                name: "",
                owner: "",
                theme: "",
                genre: "",
                country: "",
                description: ""
            })
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
            this.isShown = !this.isShown;
        },
        handleCreation() {
            if (this.creationMode === "server") {
                this.$http({
                    method: "post",
                    url: `http://${this.$store.getters.getBackendIP}:5000/server_add`,
                    data: { ...this.formData },
                }).then((response) => this.$store.commit('addServer', response.data));
            }
        }
    }
}
</script>

<style></style>