<script>
import axios from "axios";
import router from "../router";
import { decodeCredential } from "vue3-google-login";
export default {
  name: "Signup",
  data() {
    return {
      sname: "",
      email: "",
      password: "",
      name: "",
    };
  },
  methods: {
    async callback(response) {
      // decodeCredential will retrive the JWT payload from the credential
      const userData = decodeCredential(response.credential);
      console.log("Handle the userData", userData);
      this.name = userData.name;
      this.email = userData.email;
      console.log(this.email, this.name);

      let result = await axios
        .post("google/auth", {
          email: this.email,
          name: this.name,
        })
        .catch((error) => {
          // handle this error here
          alert("something is wrong!!!!!! kindly check");
          console.log(error);
        });
      if (result.status == 201) {
        alert("signing done");
        console.log(result);
        localStorage.setItem("token", result.data.token);
        console.log(result.data.token);
        this.email = "";
        this.name = "";
        this.$router.push({ name: "Home" });
      }
    },
    async signup() {
      let result = await axios.post("signup", {
        name: this.sname,
        email: this.email,
        password: this.password,
      });
      console.warn(result);
      if (result.status == 201) {
        localStorage.setItem("token", result.data.token);
        (this.sname = ""), (this.email = ""), (this.password = "");
        this.$router.push({ name: "Home" });

        alert("successfully registered.");
      } else {
        alert("user already exist!! LogIn now.");
        this.$router.push({ name: "Login" });
      }
    },
  },
  mounted() {
    let token = localStorage.getItem("token");
    if (token) {
      this.$router.push({ name: "Home" });
    } else {
      this.$router.push({ name: "Signup" });
    }
  },
};
</script>

<template>
  <div class="container">
    <div class="card w-5">
      <div class="card-header">
        <h1>SignUp Here</h1>
        <router-link :to="{ name: 'Login' }">
          <h6>Already Have an Account? Just Login</h6></router-link
        >
      </div>
      <div class="card-body">
        <form>
          <div class="mb-3">
            <label for="exampleInputName" class="form-label">Name</label>
            <input
              type="name"
              class="form-control"
              id="exampleInputname"
              aria-describedby="nameHelp"
              placeholder="Enter Name"
              v-model="sname"
            />
          </div>
          <div class="mb-3">
            <label for="exampleInputEmail1" class="form-label"
              >Email address</label
            >
            <input
              type="email"
              class="form-control"
              id="exampleInputEmail1"
              aria-describedby="emailHelp"
              placeholder="Enter Email"
              v-model="email"
            />
            <div id="emailHelp" class="form-text">
              We'll never share your email with anyone else.
            </div>
          </div>
          <div class="mb-3">
            <label for="exampleInputPassword1" class="form-label"
              >Password</label
            >
            <input
              type="password"
              class="form-control"
              id="exampleInputPassword1"
              placeholder="Enter Password"
              v-model="password"
            />
          </div>
          <div class="d-grid gap-2">
            <hr />
            <button
              class="btn btn-primary"
              type="button"
              @click.prevent="signup"
            >
              Submit
            </button>
          </div>
        </form>

        <br />

        <div class="h-100 d-flex align-items-center justify-content-center">
          <GoogleLogin :callback="callback" prompt auto-login />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  border: 0;
}
</style>