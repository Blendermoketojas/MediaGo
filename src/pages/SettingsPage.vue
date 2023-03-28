<script setup>
import BaseHeader from "../components/header/BaseHeader.vue";
import VueCarousel from 'vue-carousel';
</script>

<template>
    <body>
        <BaseHeader></BaseHeader>
        <div class="container">
            <!-- USER CATEGORY -->
            <div class="category">
                <div class="title">User</div>
                <fieldset class="category-user-fieldset">
                    <legend>Reset password</legend>

                    <!-- Password Input -->
                    <input type="password" v-model="password" placeholder="Current password" required />
                    <input type="password" v-model="password" placeholder="New password" required />
                    <input type="password" v-model="password" placeholder="Repeat password" required />
                    <button type="submit">Reset</button>
                </fieldset>
            </div>

            <!-- STYLE CATEGORY -->
            <div class="category">
                <div class="title">Style</div>
                <fieldset class="category-style-fieldset">
                    <legend>Change appearance</legend>

                    <div class="slide-box-container">
                        <div class="slide-box">
                            <v-carousel
                            style="height: 180px;"
                            hide-delimiters 
                            prev-icon="fa-solid fa-angle-left" 
                            next-icon="fa-solid fa-angle-right">

                                <template v-slot:prev="{ props }">
                                    <v-btn color="transparent" width="5px" @click="props.onClick"><i class="fa-solid fa-angle-left"></i></v-btn>
                                </template>
                                <template v-slot:next="{ props }">
                                    <v-btn color="transparent" width="5px" @click="props.onClick"><i class="fa-solid fa-angle-right"></i></v-btn>
                                </template>

                                <v-carousel-item v-for="(image, index) in images" :key="index">
                                    <img :src="image.src" :alt="image.alt">
                                </v-carousel-item>

                            </v-carousel>
                        </div>
                    </div>

                    <button type="submit">Apply</button>
                </fieldset>
            </div>
        </div>
    </body>
</template>

<script>
export default {
    data() {
        return {
            images: [
                { src: 'src/assets/selection_avatars/2th.gif', alt: 'Image 1' },
                { src: 'src/assets/selection_avatars/4th.gif', alt: 'Image 2' },
                { src: 'src/assets/selection_avatars/5th.gif', alt: 'Image 3' },
                { src: 'src/assets/selection_avatars/6th.gif', alt: 'Image 4' },
                { src: 'src/assets/selection_avatars/7th.gif', alt: 'Image 5' },
                { src: 'src/assets/selection_avatars/10th.gif', alt: 'Image 6' },
            ],
        }
    },
}
</script>

<style scoped>
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css");

body {
    background-color: #242424;
    color: white;
}

.container {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-content: center;
    width: 100%;
    padding: 10px;
    margin-top: 100px;
}

.title {
    font-weight: bold;
    text-transform: uppercase;
    font-size: 30px;
    text-align: left;
    color: #04aa6d;
}

.category-user-fieldset {
    border: 1px solid #04aa6d;
    border-radius: 10px;
    padding: 20px;
    margin: 10px;
    width: 70%;
}

.category-style-fieldset {
    border: 1px solid #04aa6d;
    border-radius: 10px;
    padding: 20px;
    margin: 10px;
    width: 400px;
}

.category-fieldset legend {
    font-size: 20px;
}

.category {
    padding: 15px;
}

input {
    width: 100%;
    padding: 9px 10px;
    margin: 8px 0;
    background-color: transparent;
    color: white;
    outline: none;
    outline-style: none;
    border-top: none;
    border-left: none;
    border-right: none;
    border-bottom: 1px solid #04aa6d;
    padding: 3px 10px;
}

input:focus {
    outline: none !important;
    border-bottom: 1px solid #04aa6d;
    box-shadow: 0px 1px 0px #04aa6d;
}

button {
    background-color: #04aa6d;
    color: white;
    padding: 9px 20px;
    margin: 15px 0 0px;
    border: none;
    cursor: pointer;
    width: 100%;
    font-size: 15px;
    font-weight: 400;
    text-transform: uppercase;
    border-radius: 5px;
}

.slide-box img {
    width: 160px;
    height: 160px;
}

.slide-box-container {
    width: 150px;
    margin: auto;
}

.btn-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 10px;
}

.btn-container i {
    padding-left: 15px;
    padding-right: 15px;
    color: white;
}

</style>