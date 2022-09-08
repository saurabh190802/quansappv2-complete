<script>
import axios from "axios";
export default {
  name: "Home",
  data() {
    return {
      username: "",
      trackername: "",
      desc: "",
      trackertype: "",
      alltrackers: [],
      uptrackertype: "",
      uptrackername: "",
      updesc: "",
      upid: 0,
      value: "",
      note: "",
      pdfurl: "",
      csvurl: "",
    };
  },
  methods: {
    async gettrackercsv() {
      const result = await axios
        .get("export/trackercsv", {
          headers: {
            "x-access-token": localStorage.getItem("token"),
          },

          responseType: "blob",
        })
        .catch((error) => {
          // handle this error here
          alert("wrong");
        });
      if (result.status == 200) {
        alert("done");
        console.log(result);
        const downloadUrl = window.URL.createObjectURL(new Blob([result.data]));
        this.csvurl = downloadUrl;
        const link = document.createElement("a");
        link.href = this.csvurl;

        link.setAttribute("download", this.username + "_AllTrackers" + ".csv");
        document.body.appendChild(link);
        link.click();
        link.remove();
      }
    },
    async gettrackerpdf() {
      const result = await axios
        .get("export/trackerpdf", {
          headers: {
            "x-access-token": localStorage.getItem("token"),
          },

          responseType: "blob",
        })
        .catch((error) => {
          // handle this error here
          //alert("wrong");
          alert(
            "Not supported on Heroku🥲🥲😔😓 But No worries We'll do some hack for you soon.."
          );
        });
      if (result.status == 200) {
        alert("done");
        console.log(result);
        const downloadUrl = window.URL.createObjectURL(new Blob([result.data]));
        this.pdfurl = downloadUrl;
        const link = document.createElement("a");
        link.href = this.pdfurl;

        link.setAttribute("download", this.username + "_AllTrackers" + ".pdf");
        document.body.appendChild(link);
        link.click();
        link.remove();
      }
    },
    directtotd(tracker) {
      this.$router.push({
        name: "TrackerDashboard",
        params: { data: tracker.id },
      });
    },
    logout() {
      localStorage.removeItem("token");
      this.$router.push("login");
    },
    async addtracker() {
      let result = await axios
        .post(
          "addtracker",
          {
            name: this.trackername,
            desc: this.desc,
            trackertype: this.trackertype,
          },
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
        this.$router.go(this.$router.currentRoute);
        alert("tracker added");
        this.trackername = "";
        this.desc = "";
        this.trackertype = "";
      } else {
        alert("tracker not added!!! something wrong");
      }
    },
    async deletetracker(id) {
      let result = await axios
        .delete(
          "deltracker/" + id,

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
        this.$router.go(this.$router.currentRoute);
        alert("tracker deleted");
      }
    },
    async deletealltrackers() {
      let result = await axios
        .delete(
          "delalltrackers",

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
        this.$router.go(this.$router.currentRoute);
        alert("all trackers deleted");
      }
    },
    handleupdateform(tracker) {
      this.updesc = tracker.desc;
      this.uptrackername = tracker.name;
      this.uptrackertype = tracker.trackertype;
      this.upid = tracker.id;
    },
    async updatetracker(id) {
      let result = await axios
        .post(
          "updatetracker/" + id,
          {
            name: this.uptrackername,
            desc: this.updesc,
            trackertype: this.uptrackertype,
          },

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
        this.$router.go(this.$router.currentRoute);
        alert("tracker updated");
      }
    },
    async addlog(trackername) {
      let result = await axios
        .post(
          trackername + "/log",
          {
            value: this.value,
            note: this.note,
          },
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
        alert("added");
        this.$router.go(this.$router.currentRoute);
      } else {
        alert("tracker not added!!! something wrong");
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
      console.log(result);
      console.log(this.username);
    }
    const trackersres = await axios.get("trackers", {
      headers: {
        "x-access-token": localStorage.getItem("token"),
      },
    });
    if (trackersres.status == 200) {
      this.alltrackers = trackersres.data.trackers;
      console.log(this.alltrackers);
    }
  },
};
</script>
<template>
  <nav
    class="navbar navbar-expand-lg navbar-dark"
    style="background-color: rgba(0, 0, 0, 0.5)"
  >
    <div class="container-fluid">
      <a class="navbar-brand" href="#"
        ><router-link :to="{ name: 'Profile' }" class="routerLink"
          ><h4>Hi, {{ username }}</h4></router-link
        ></a
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
          <li class="nav-item"></li>
        </ul>
        <button type="button" class="btn btn-danger" @click="logout">
          Log Out
        </button>
      </div>
    </div>
  </nav>
  <div class="container">
    <div class="d-grid gap-2">
      <br />

      <button
        class="btn btn-primary"
        type="button"
        data-bs-toggle="modal"
        data-bs-target="#exampleModal"
      >
        <h2>Add a New Tracker</h2>
      </button>
      <br />
    </div>
    <div>
      <label><h2 style="color: white">Your Trackers</h2> </label>
      <button
        type="button"
        class="btn btn-secondary"
        data-bs-toggle="modal"
        data-bs-target="#exampleModalexport"
        style="float: right"
      >
        Export Data
      </button>
    </div>
    <br />

    <div class="container">
      <div class="table-responsive">
        <table
          class="table table-dark table-hover"
          v-if="alltrackers.length > 0"
        >
          <thead>
            <tr>
              <th scope="col">SNo.</th>
              <th scope="col">Name</th>
              <th scope="col">Description</th>
              <th scope="col">Type</th>
              <th scope="col">Settings</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(tracker, index) in alltrackers" :key="tracker.id">
              <th scope="row">{{ index }}</th>

              <td @click="directtotd(tracker)" style="cursor: pointer">
                {{ tracker.name }}
              </td>
              <td>{{ tracker.desc }}</td>
              <td>{{ tracker.trackertype }}</td>
              <td>
                <div
                  class="btn-group"
                  role="group"
                  aria-label="Basic mixed styles example"
                >
                  <button
                    type="button"
                    class="btn btn-success"
                    data-bs-toggle="modal"
                    data-bs-target="#exampleModaladdlog"
                    @click="handleupdateform(tracker)"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      fill="currentColor"
                      class="bi bi-plus-circle"
                      viewBox="0 0 16 16"
                    >
                      <path
                        d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"
                      />
                      <path
                        d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"
                      />
                    </svg>
                  </button>
                  <button
                    type="button"
                    class="btn btn-warning"
                    data-bs-toggle="modal"
                    data-bs-target="#exampleModalupdate"
                    @click="handleupdateform(tracker)"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      fill="currentColor"
                      class="bi bi-pen"
                      viewBox="0 0 16 16"
                    >
                      <path
                        d="m13.498.795.149-.149a1.207 1.207 0 1 1 1.707 1.708l-.149.148a1.5 1.5 0 0 1-.059 2.059L4.854 14.854a.5.5 0 0 1-.233.131l-4 1a.5.5 0 0 1-.606-.606l1-4a.5.5 0 0 1 .131-.232l9.642-9.642a.5.5 0 0 0-.642.056L6.854 4.854a.5.5 0 1 1-.708-.708L9.44.854A1.5 1.5 0 0 1 11.5.796a1.5 1.5 0 0 1 1.998-.001zm-.644.766a.5.5 0 0 0-.707 0L1.95 11.756l-.764 3.057 3.057-.764L14.44 3.854a.5.5 0 0 0 0-.708l-1.585-1.585z"
                      />
                    </svg>
                  </button>

                  <button
                    type="button"
                    class="btn btn-danger"
                    @click="deletetracker(tracker.id)"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      fill="currentColor"
                      class="bi bi-trash"
                      viewBox="0 0 16 16"
                    >
                      <path
                        d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"
                      />
                      <path
                        fill-rule="evenodd"
                        d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"
                      />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <br />
    <div class="d-grid gap-2" v-if="alltrackers.length > 0">
      <button class="btn btn-danger" type="button" @click="deletealltrackers()">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          fill="currentColor"
          class="bi bi-trash"
          viewBox="0 0 16 16"
        >
          <path
            d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"
          />
          <path
            fill-rule="evenodd"
            d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"
          />
        </svg>
        &nbsp;Delete All Trackers
      </button>
    </div>
  </div>
  <div class="container">
    <div class="alert alert-danger" role="alert" v-if="alltrackers.length == 0">
      No Tracker Found!!!!!!! Track something from now.
    </div>
  </div>

  <!--Tracker add Modal -->
  <div
    class="modal fade"
    id="exampleModal"
    tabindex="-1"
    aria-labelledby="exampleModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">Add a New Tracker</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <form>
            <div class="mb-3">
              <label for="exampleInputEmail1" class="form-label"
                >Tracker Name</label
              >
              <input
                type="name"
                class="form-control"
                id="exampleInputEmail1"
                aria-describedby="nameHelp"
                v-model="trackername"
              />
            </div>
            <div class="mb-3">
              <label for="exampleFormControlTextarea1">Description</label>
              <textarea
                class="form-control"
                id="exampleFormControlTextarea1"
                rows="3"
                v-model="desc"
              ></textarea>
            </div>
            <div class="mb-3">
              <label for="exampleInputEmail1" class="form-label"
                >Tracker Type</label
              >

              <select
                class="form-select"
                aria-label="Default select example"
                v-model="trackertype"
              >
                <option selected>Choose from below</option>
                <option value="Numerical">Numerical</option>
                <option value="Multiple">Multiple</option>
                <option value="Time Duration">Time Duration</option>
                <option value="Boolean">Boolean</option>
              </select>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Close
          </button>
          <button
            type="button"
            class="btn btn-primary"
            data-bs-dismiss="modal"
            @click="addtracker"
          >
            Save
          </button>
        </div>
      </div>
    </div>
  </div>
  <!-- Modal update tracker-->
  <div
    class="modal fade"
    id="exampleModalupdate"
    tabindex="-1"
    aria-labelledby="exampleModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">Update Tracker</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <form>
            <div class="mb-3">
              <label for="exampleInputEmail1" class="form-label"
                >Tracker Name</label
              >
              <input
                type="name"
                class="form-control"
                id="exampleInputEmail1"
                aria-describedby="nameHelp"
                v-model="uptrackername"
              />
            </div>
            <div class="mb-3">
              <label for="exampleFormControlTextarea1">Description</label>
              <textarea
                class="form-control"
                id="exampleFormControlTextarea1"
                rows="3"
                v-model="updesc"
              ></textarea>
            </div>
            <div class="mb-3">
              <label for="exampleInputEmail1" class="form-label"
                >Tracker Type</label
              >
              <select
                class="form-select"
                aria-label="Default select example"
                v-model="uptrackertype"
              >
                <option selected>Choose from below</option>
                <option value="Numerical">Numerical</option>
                <option value="Multiple">Multiple</option>
                <option value="Time Duration">Time Duration</option>
                <option value="Boolean">Boolean</option>
              </select>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Close
          </button>
          <button
            type="button"
            class="btn btn-primary"
            @click="updatetracker(upid)"
          >
            Update
          </button>
        </div>
      </div>
    </div>
  </div>
  <!-- Modal add new log -->
  <div
    class="modal fade"
    id="exampleModaladdlog"
    tabindex="-1"
    aria-labelledby="exampleModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">
            Log to {{ uptrackername }}
          </h5>

          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <form>
            <div class="mb-3">
              <label for="exampleInputEmail1" class="form-label"
                >Value (Type: {{ uptrackertype }})
              </label>
              <input
                type="number"
                class="form-control"
                id="exampleInput"
                aria-describedby="Help"
                v-model="value"
                v-if="uptrackertype == 'Numerical'"
              />
              <input
                type="number"
                class="form-control"
                id="exampleInput"
                aria-describedby="Help"
                v-model="value"
                v-if="uptrackertype == 'Time Duration'"
                placeholder="Give duration in minutes"
              />
              <input
                type="value"
                class="form-control"
                id="exampleInput"
                aria-describedby="Help"
                v-model="value"
                v-if="uptrackertype == 'Multiple'"
                placeholder="Separate values with comma(',')"
              />
              <select
                class="form-select"
                aria-label="Default select example"
                v-model="value"
                v-if="uptrackertype == 'Boolean'"
              >
                <option selected>Choose from Below</option>
                <option value="Yes">Yes</option>
                <option value="No">No</option>
              </select>
            </div>
            <div class="mb-3">
              <label for="exampleInputPassword1" class="form-label">Note</label>
              <input
                type="text"
                class="form-control"
                id="exampleInputPassword1"
                v-model="note"
              />
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Close
          </button>
          <button
            type="button"
            class="btn btn-primary"
            @click="addlog(uptrackername)"
          >
            Save
          </button>
        </div>
      </div>
    </div>
  </div>
  <!-- export modal -->
  <div class="modal" id="exampleModalexport" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Export</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <div class="d-grid gap-2">
            <button class="btn btn-info" type="button" @click="gettrackerpdf()">
              Export As .pdf
            </button>
            <button class="btn btn-info" type="button" @click="gettrackercsv()">
              Export As .csv
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
.routerLink {
  text-decoration: none;
  color: antiquewhite;
}
</style>
