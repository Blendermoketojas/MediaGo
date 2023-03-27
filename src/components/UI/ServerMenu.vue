<template>
    <div class="d-flex flex-row custom-color justify-content-between" style="margin-top: 4rem; height: 3.5rem">
        <div class="d-flex align-items-center">
            <span class="ms-5 custom-font text-white">Filter servers</span>
        </div>
        <div class="d-flex flex-row align-items-center">
            <v-card class="me-3">
                <select v-model="formData.popular" style="width: 150px; height: 40px" class="form-select border-0">
                    <option :value="true">Most popular</option>
                    <option :value="false">Least popular</option>
                </select>
            </v-card>
            <v-card class="me-3">
                <select v-model="formData.country" style="width: 160px; height: 40px" class="form-select border-0">
                    <option :value="0">All countries</option>
                    <option v-for="country in this.$store.getters.getCountries" :value="country.id">{{ country.name }}
                    </option>
                </select>
            </v-card>
            <v-card class="me-3">
                <select v-model="formData.genre" style="width: 150px; height: 40px" class="form-select border-0">
                    <option selected :value="0">All genres</option>
                    <option v-for="genre in this.$store.getters.getGenres" :value="genre.id">{{ genre.name }}</option>
                </select>
            </v-card>
            <v-card class="me-3">
                <select v-model="formData.limit" style="width: 100px; height: 40px" class="form-select border-0">
                    <option selected :value="10">10</option>
                    <option :value="25">25</option>
                    <option :value="50">50</option>
                </select>
            </v-card>
            <div class="text-center">
                <v-pagination class="text-white" v-model="page" :length="this.$store.getters.getPageCount" :total-visible="5"></v-pagination>
            </div>
        </div>
    </div>
</template>
  
<script>
import { reactive } from 'vue';

export default {
    emits: ['fetchServers'],
    props: {

    },
    data() {
        return {
            formData: {
                popular: true,
                country: 0,
                genre: 0,
                limit: 10,
                offset: 0,
            },
            formReq: {

            },
            page: 1,
            countries: null,
            genres: null,
        };
    },
    computed: {

    },
    watch: {
        page(newVal, oldVal) {
            this.formData.offset = this.formData.limit * (newVal - 1);
            this.makeRequest();
        },
        'formData.popular': function (newVal, oldVal) {
            this.makeRequest();
        },
        'formData.country': function (newVal, oldVal) {
            this.makeRequest();
        },
        'formData.genre': function (newVal, oldVal) {
            this.makeRequest();
        },
        'formData.limit': function (newVal, oldVal) {
            this.makeRequest();
        },
    },
    methods: {
        fetchGenres() {
            this.$http({
                method: "get",
                url: `https://${this.$store.getters.getBackendIP}:5000/get_dropdown_search?type=genre`,
            }).then((response) => { this.$store.commit('setGenres', response.data.data); this.fetchCountries() });
        },
        fetchCountries() {
            this.$http({
                method: "get",
                url: `https://${this.$store.getters.getBackendIP}:5000/get_dropdown_search?type=country`,
            }).then((response) => this.$store.commit('setCountries', response.data.data));
        },
        onFormDataChange(obj) {
            this.formReq = { ...this.formReq, ...obj }
        },
        makeRequest() {
            var tempRequest;
            if (this.formData.country == 0 && this.formData.genre == 0) {
                tempRequest = { popular: this.formData.popular, offset: this.formData.offset, limit: this.formData.limit }
            } else if (this.formData.country == 0) {
                tempRequest = { popular: this.formData.popular, offset: this.formData.offset, limit: this.formData.limit, genre: this.formData.genre }
            } else if (this.formData.genre == 0) {
                tempRequest = { popular: this.formData.popular, offset: this.formData.offset, limit: this.formData.limit, country: this.formData.country }
            } else {
                tempRequest = { ...this.formData }
            }
            this.$http({
                method: "post",
                data: {
                    ...tempRequest
                },
                url: `https://${this.$store.getters.getBackendIP}:5000/get_servers`,
            }).then((response) => { this.$store.commit('setServers', response.data.data); this.$store.commit('setPageCount', response.data.pages)});
        }
    },
    mounted() {
        if (!this.$store.getters.getCountries || !this.$store.getters.getGenres) {
            this.fetchGenres();
        }
        if (!this.$store.getters.getServers) {
            this.makeRequest();
        }
    }
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