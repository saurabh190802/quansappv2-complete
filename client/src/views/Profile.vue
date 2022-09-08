<template>
  <nav
    class="navbar navbar-expand-lg navbar-dark"
    style="background-color: rgba(0, 0, 0, 0.5)"
  >
    <div class="container-fluid">
      <a class="navbar-brand" href="#"
        ><h4>Hi, {{ this.username }}</h4></a
      >
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarText"
        aria-controls="navbarText"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarText">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link :to="{ name: 'Home' }"
              ><button type="button" class="btn btn-primary">
                Home
              </button></router-link
            >
          </li>
        </ul>
        <button type="button" class="btn btn-danger" @click="logout()">
          Log Out
        </button>
      </div>
    </div>
  </nav>
  <div class="container">
    <div class="d-grid gap-2">
      <br />

      <div class="card text-center">
        <div class="card-header">Your Details</div>
        <div class="card-body">
          <h5 class="card-title">Name: {{ this.username }}</h5>
          <h5 class="card-title">Email: {{ this.email }}</h5>

          <button class="btn btn-danger" @click="deleteuser">
            Delete Account
          </button>
        </div>
        <div class="card-footer text-muted">
          <h6 style="color: white">
            Joined at: {{ this.joined }} || Last Visit: {{ this.lastvisit }}
          </h6>
        </div>
      </div>
      <br />
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "Home",
  data() {
    return {
      username: "",
      email: "",
      joined: "",
      lastvisit: "",
    };
  },
  methods: {
    logout() {
      localStorage.removeItem("token");
      this.$router.push("login");
    },
    async deleteuser() {
      let result = await axios
        .delete(
          "deleteuser",

          {
            headers: {
              "x-access-token": localStorage.getItem("token"),
            },
          }
        )
        .catch((error) => {
          // handle this error here
          alert("something is wrong!!!!!! kindly check");
        });

      if (result.status == 200) {
        localStorage.removeItem("token");
        this.$router.push("/");
        alert("user deleted");
      }
    },
  },

  mounted() {
    let token = localStorage.getItem("token");
    if (!token) {
      this.$router.push({ name: "Welcome" });
    }
  },
  async created() {
    const result = await axios
      .get("user", {
        headers: {
          "x-access-token": localStorage.getItem("token"),
        },
      })
      .catch((error) => {
        // handle this error here
        alert("Time Out");
        localStorage.removeItem("token");
        this.$router.push("login");
      });
    if (result.status == 200) {
      this.username = result.data.user.name;
      this.email = result.data.user.email;
      this.joined = result.data.user.joined;
      this.lastvisit = result.data.user.lastvisit;
      console.log(result);
      console.log(this.username);
    }
  },
};
</script>

<style></style>