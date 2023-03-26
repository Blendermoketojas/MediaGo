<template>
    <div class="pointer-on-click">
        <span class="me-2">{{ username }}</span>
        <v-avatar color="surface-variant">
            <img style="width:150%;" :src="userImg" />
            <v-menu class="mt-1" activator="parent">
                <v-list>
                    <v-list-item>
                        <v-btn @click="handleSignOut">
                            <v-list-item-title>Sign out</v-list-item-title>
                        </v-btn>
                    </v-list-item>
                </v-list>
            </v-menu>
        </v-avatar>
    </div>
</template>

<script>
import userImgAvatar from '../../assets/catuser.png';

export default {
    data() {
        return {
            userImg: userImgAvatar
        }
    },
    props: {
        username: {
            type: String,
            required: true
        }
    },
    methods: {
        handleSignOut() {
            sessionStorage.clear('user');
            this.$store.dispatch('logout');
            this.$router.push({ path: '/authentication' })
        }
    }
}
</script>

<style>
.pointer-on-click {
    cursor: pointer;
}
</style>