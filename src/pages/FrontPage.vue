<template>
  <div class="container w-25">

    <!-- LOGIN FORM -->
    <form v-if="!showRegisterForm">

      <!-- Form Title -->
      <h1 id="form-title">LOGIN</h1>

      <!-- Email Input -->
      <input type="email" v-model="formData.email" placeholder="Enter Email" />

      <!-- Password Input -->
      <input type="password" v-model="formData.password" placeholder="Enter password" />

      <!-- Submit Button -->
      <button type="submit">Login</button>
      <p>Not a member? <a href="#!" @click="toggleRegisterForm">Register</a></p>

    </form>

    <!-- ------------------------------------------------------------------------------------- -->

    <!-- REGISTER FORM -->
    <form v-else>

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
      <p>Already have account? <a href="#!" @click="toggleRegisterForm">Login</a></p>
    </form>
  </div>
</template>

<script>
import { reactive } from "vue";
export default {
  data() {
    return {
      showRegisterForm: false,
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
        url: "BACKEND_URL",
        data: { ...this.formData },
      }).then((response) => console.log(response.data));
    },
    toggleRegisterForm() {
      this.showRegisterForm = !this.showRegisterForm;
    },
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Tilt+Neon&display=swap");

.container {
  font-family: "Tilt Neon", cursive;
  border: solid black 1px;
  background: #1f1f1e;
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
input[type="password"] {
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