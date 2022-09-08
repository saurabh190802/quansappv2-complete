<template>
  <div class="container">
    <div class="card text-center">
      <div class="card-header">Reset Password</div>
      <div class="card-body">
        <form v-if="!isOTP">
          <div class="mb-3">
            <label for="exampleInputEmail1" class="form-label"
              >Email address</label
            >
            <input
              type="email"
              class="form-control"
              id="exampleInputEmail1"
              aria-describedby="emailHelp"
              v-model="email"
            />
          </div>
          <button
            type="submit"
            class="btn btn-primary"
            @click.prevent="handlegenerateotp()"
          >
            Generate OTP
          </button>
        </form>
        <form v-if="isOTP">
          <div class="container">
            <div class="mb-3">
              <label for="exampleInputEmail1" class="form-label"
                >Enter OTP</label
              >
              <input
                type="number"
                class="form-control"
                id="exampleInputotp"
                aria-describedby="numberHelp"
                v-model="otp"
              />
              <br />

              <label for="exampleInputEmail1" class="form-label"
                >Enter New Password</label
              >
              <input
                type="password"
                class="form-control"
                id="exampleInputotp"
                aria-describedby="numberHelp"
                v-model="newpassword"
              />
            </div>
            <button
              type="submit"
              class="btn btn-primary"
              @click.prevent="changepwd()"
            >
              Save</button
            ><br /><br />
            <a
              style="
                cursor: pointer;
                color: ghostwhite;
                text-decoration: underline;
              "
              >Resend OTP</a
            >
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "Resetpwd",
  data() {
    return {
      isOTP: false,
      email: "",
      otp: "",
      newpassword: "",
    };
  },
  methods: {
    async handlegenerateotp() {
      if (this.email.length !== 0) {
        const result = await axios
          .get(this.email + "/generateotp")
          .catch((error) => {
            // handle this error here
            alert("wrong");
          });
        if (result.status == 201) {
          alert("otpsent");
          console.log(result)
          this.isOTP = !this.isOTP;
        }
      }
    },
    async changepwd() {
      let result = await axios
        .post("resetpassword", {
          email: this.email,
          otp: this.otp.toString(),
          password: this.newpassword,
        })
        .catch((error) => {
          // handle this error here
          alert("something is wrong!!!!!! kindly check");
          
        });

      if (result.status == 201) {
        this.$router.push({ name: "Login" });
        
        alert("Password Changed Now Login");
        this.email = "";
        this.otp = "";
        this.newpassowrd = "";
      } else {
        alert("password not changed!!! something wrong");
      }
    },
  },
};
</script>

<style>
.card {
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  border: 0;
}
</style>