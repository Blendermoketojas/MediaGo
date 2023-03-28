<template>
  <div class="vh-100 vw-100 d-flex justify-content-center align-items-center" style="background-color: #121313;">
    <div class="container_auth" style="width: 33%;">

      <!-- LOGIN FORM -->
      <!-- @submit.prevent="handleLogin" -->
      <form @submit="checkLoginForm" v-if="!showRegisterForm">

        <h1 id="form-title">LOGIN</h1>
        <input type="text" v-model="formData.email" placeholder="Enter Email"/>
        <input type="password" v-model="formData.password" placeholder="Enter password"/>
        <button type="submit">Login</button>

        <!-- <span v-if="this.errors" style="color: crimson;">An ERROR occured: {{ this.message }}</span> -->
        <p>Not a member? <a href="#!" @click="toggleRegisterForm">Register</a></p>

      </form>

      <!-- REGISTER FORM -->
      <!-- @submit.prevent="handleRegistration" -->
      <form @submit="checkRegisterForm" v-else>

        <h1 id="form-title">REGISTER</h1>
        <input type="text" v-model="formData.nickname" placeholder="Nickname" />
        <input type="text" v-model="formData.email" placeholder="Email" />
        <input type="password" v-model="formData.password" placeholder="Enter password" />
        <button type="submit">Register</button>

        <!-- <span v-if="this.errors" style="color: crimson;">An ERROR occured: {{ this.message }}</span> -->
        <p>Already have account? <a href="#!" @click="toggleRegisterForm">Login</a></p>

      </form>

      <!-- VALIDATION VIEW -->
      <p v-if="errors.length > 0">
        <b>Please correct the following error(s):</b>
        <ul>
          <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
        </ul>
      </p>

    </div>
  </div>
</template>

<script>

import { reactive } from "vue";
export default {
  data() {
    return {
      showRegisterForm: false,
      // errors: false,
      errors: [],
      // message: '',
      formData: reactive({
        nickname: null,
        email: null,
        password: null,
      }),
    };
  },
  methods: {

    toggleRegisterForm() {
      this.errors = [];
      this.showRegisterForm = !this.showRegisterForm;
    },
    
    checkLoginForm: function (e) {
      this.errors = [];
      this.errors = this.errors.concat(this.validateEmail());
      this.errors = this.errors.concat(this.loginValidatePassword());
      if (this.errors.length > 0) {
        e.preventDefault();
      } else {
        this.handleLogin();
        e.preventDefault();
      }
    },

    checkRegisterForm: function (e) {
      this.errors = [];
      this.errors = this.errors.concat(this.validateNickname());
      this.errors = this.errors.concat(this.validateEmail());
      this.errors = this.errors.concat(this.registerValidatePassword());
      if (this.errors.length > 0) { 
        e.preventDefault();
      } else{
        this.handleRegistration();
        e.preventDefault();
      }
    },

    handleLogin() {
      this.$http({
        method: "post",
        url: `http://${this.$store.getters.getBackendIP}:5000/login`,
        data: { email: this.formData.email, password: this.formData.password },
      }).then((response) => this.handleUserInitialization(response.data));
    },

    handleRegistration() {
      this.$http({
        method: "post",
        url: `http://${this.$store.getters.getBackendIP}:5000/register`,
        data: { ...this.formData },
      }).then((response) => this.handleUserInitialization(response.data));
    },

    handleUserInitialization(data) {
      this.errors = [];
      if (data.success) {
        console.log("request success");
        this.$store.commit('setUser', { id: data.id, name: data.nickname });
        this.$store.commit('setIsAuthenticated', true);
        sessionStorage.setItem('user', JSON.stringify({ id: data.id, name: data.nickname }));
        this.$router.push({ path: '/floor/waiting_room' });
      } else {
        console.log("request not success");
        this.errors.push("An Error occurred.");
        // this.message = data.message;
        console.log("DATA: ", + this.formData.nickname + " " + this.formData.email + " " + this.formData.password);
      }
    },

    validateNickname() {
      let err = [];
      const nicknameRegex = new RegExp("^[a-zA-Z0-9_]+$");

      if (this.formData.nickname == null || this.formData.nickname == "") {
        err.push("Nickname must be filled out");
        return err;
      }      

      if (!nicknameRegex.test(this.formData.nickname))
        err.push("Nickname can only contain letters, digits, and underscores (_)");

      if (this.formData.nickname.length < 5)
        err.push("Nickname must be at least 5 characters long");

      return err;
    },

    validateEmail() {
      let err = [];
      const emailRegex = new RegExp("^[\\w-\\.]+@([\\w-]+\\.)+[\\w-]{2,}$");

      if (this.formData.email == null || this.formData.email == "") {
        err.push("Email must be filled out");
        return err;
      }

      if (!emailRegex.test(this.formData.email)) 
        err.push("Provided email is invalid.");

      return err;
    },

    registerValidatePassword() {
      let err = [];
      const digitRegex = new RegExp("\\d");
      const lowercaseRegex = new RegExp("[a-z]");
      const uppercaseRegex = new RegExp("[A-Z]");
      const specialCharRegex = new RegExp("[!@#\\$%\\^&\\*]");

      if (this.formData.password == null || this.formData.password == "") {
        err.push("Password must be filled out");
        return err;
      }

      if (!digitRegex.test(this.formData.password))
        err.push("Password must be at least 1 digit");

      if (!lowercaseRegex.test(this.formData.password))
        err.push("Password must be at least 1 lowercase letter");

      if (!uppercaseRegex.test(this.formData.password))
        err.push("Password must be at least 1 uppercase letter");

      if (!specialCharRegex.test(this.formData.password))
        err.push("Password must be at least 1 special character");

      return err;
    },

    loginValidatePassword() {
      let err = [];
      if (this.formData.password == null || this.formData.password == "")
        err.push("Password must be filled out");
        
      return err;
    },
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

input {
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

ul {
  list-style: none; /* Remove default bullets */
}

ul li::before {
  content: "\2022";
  color: #04aa6d;
  font-weight: bold;
  display: inline-block;
  width: 2em;
  margin-left: -2em;
}
</style>