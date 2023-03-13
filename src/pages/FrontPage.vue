<template>
  <div class="vh-100 vw-100 d-flex justify-content-center align-items-center" style="background-color: #121313;">
    <div class="container_auth" style="width: 33%;">

      <!-- LOGIN FORM -->
      <form @submit.prevent="handleLogin" v-if="!showRegisterForm">

        <!-- Form Title -->
        <h1 id="form-title">LOGIN</h1>

        <!-- Email Input -->
        <input type="email" v-model="formData.email" placeholder="Enter Email" />

        <!-- Password Input -->
        <input type="password" v-model="formData.password" placeholder="Enter password" />

        <!-- Submit Button -->
        <button type="submit">Login</button>
        <span v-if="this.errors" style="color: crimson;">An ERROR occured: {{ this.message }}</span>
        <p>Not a member? <a href="#!" @click="toggleRegisterForm">Register</a></p>
      </form>

      <!-- ------------------------------------------------------------------------------------- -->

      <!-- REGISTER FORM -->
      <form @submit.prevent="handleRegistration" v-else>

        <!-- Form Title -->
        <h1 id="form-title">REGISTER</h1>

        <!-- Username Input -->
        <input type="text" v-model="formData.nickname" placeholder="Username" />

        <!-- Email Input -->
        <input type="email" v-model="formData.email" placeholder="Email" />

        <!-- Password Input -->
        <input type="password" v-model="formData.password" placeholder="Enter password" />

        <!-- Submit Button -->
        <button type="submit">Register</button>
        <span v-if="this.errors" style="color: crimson;">An ERROR occured: {{ this.message }}</span>
        <p>Already have account? <a href="#!" @click="toggleRegisterForm">Login</a></p>
      </form>
    </div>
  </div>
</template>

<script>

import { reactive } from "vue";
export default {
  data() {
    return {
      showRegisterForm: false,
      errors: false,
      message: '',
      formData: reactive({
        nickname: "",
        email: "",
        password: "",
      }),
     
    };
  },
  methods: {
    handleLogin() {
      this.$http({
        method: "post",
        url: `http://${this.$store.getters.getBackendIP}:5000/login`,
        data: { ...this.formData },
      }).then((response) => this.handleUserInitialization(response.data));
    },
    toggleRegisterForm() {
      this.showRegisterForm = !this.showRegisterForm;
    },
    handleRegistration() {
      this.$http({
        method: "post",
        url: `http://${this.$store.getters.getBackendIP}:5000/register`,
        data: { ...this.formData },
      }).then((response) => this.handleUserInitialization(response.data));
    },
    handleUserInitialization(data) {
      if (data.success) {
        console.log("request success")
        this.$store.commit('setUser', { id: data.id, name: data.nickname });
        sessionStorage.setItem('user', { id: data.id, name: data.nickname });
        this.$router.push({ path: '/floor/waiting_room' })
      } else {
        console.log("request not success")
        this.errors = true;
        this.message = data.message;
      }
    },
    // handleAuthentication() {
    //   if(this.showRegisterForm) {

    //   } else {
    //     this.handleLogin();
    //   }
    // },
    validate() {
    }
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Tilt+Neon&display=swap");

.container_auth {
  font-family: "Tilt Neon", cursive;
  border: solid black 1px;
  background-color: #1f1f1e;
  padding: 15px;
}

#form-title {
  font-weight: bold;
  font-size: 40px;
  text-align: center;
  color: #04aa6d;
}

button:hover {
  opacity: 0.8;
}

p {
  color: #757575;
}

input[type="text"],
input[type="password"],
input[type="email"] {
  width: 100%;
  padding: 10px 10px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #04aa6d;
  box-sizing: border-box;
  background-color: #1f1f1e;
  color: white;
}

input:focus {
  outline: none !important;
  border: 1px solid #04aa6d;
  box-shadow: 0 0 5px #04aa6d;
}

button {
  background-color: #04aa6d;
  color: white;
  padding: 10px 20px;
  margin: 15px 0px;
  border: none;
  cursor: pointer;
  width: 100%;
  font-size: 15px;
  text-transform: uppercase;
  border-radius: 5px;
}

.rememberMe {
  color: white;
  font-size: small;
}
</style>