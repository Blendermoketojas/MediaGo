<template>
    <div class="d-flex flex-row custom-color justify-content-between" style="margin-top: 4rem; height: 3.5rem">
        <div class="d-flex align-items-center">
            <span class="ms-5 custom-font text-white">Filter servers</span>
        </div>
        <div class="d-flex flex-row align-items-center">
            <v-card class="me-3">
                <select style="width: 200px; height: 40px" class="form-select border-0">
                    <option :value="true">Most popular</option>
                    <option :value="false">Least popular</option>
                </select>
            </v-card>
            <v-card class="me-3">
                <select style="width: 200px; height: 40px" class="form-select border-0">
                    <option>Find by country</option>
                    <option>Germany</option>
                    <option>France</option>
                </select>
            </v-card>
            <v-card class="me-3">
                <select style="width: 200px; height: 40px" class="form-select border-0">
                    <option>Find by genre</option>
                    <option>Rock</option>
                    <option>Disco</option>
                </select>
            </v-card>
            <v-card class="me-3">
                <select style="width: 200px; height: 40px" class="form-select border-0">
                    <option>Limit</option>
                    <option>10</option>
                    <option>25</option>
                    <option>50</option>
                </select>
            </v-card>
            <div class="text-center">
                <v-pagination class="text-white" v-model="page" :length="15" :total-visible="5"></v-pagination>
            </div>
        </div>
    </div>
</template>
  
<script>
import { reactive } from 'vue';

export default {
    props: {

    },
    data() {
        return {
            formData: reactive({
                popular: null,
                country: null,
                genre: null,
                limit: 10,
                offset: null
            }),
            page: 1,
        }
    },
    watch: {
        page: {
            handler(newVal, oldVal) {
                console.log("offset: " + this.formData.limit * (newVal - 1))
                this.formData.offset = this.formData.limit * (newVal - 1);
            }
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