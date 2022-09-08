<script>
import { useRoute } from "vue-router";
import axios from "axios";

export default {
  name: "TrackerDashboard",

  data() {
    return {
      tracker_id: 0,
      cur_tracker: [],
      logs: [],
      username: "",
      upvalue: "",
      upnote: "",
      uptimestamp: "",
      uplogid: 0,
      value: "",
      note: "",
      pdfurl: "",
      tracker_lastused: "",
      plot_url: "",
    };
  },
  destroyed() {
    this.tracker_id = 0;
  },
  methods: {
    async getlogcsv(tracker_name) {
      const result = await axios
        .get("export/" + tracker_name + "/logcsv", {
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

        link.setAttribute(
          "download",
          this.username + "_" + tracker_name + "_AllLogs" + ".csv"
        );
        document.body.appendChild(link);
        link.click();
        link.remove();
      }
    },
    async getlogpdf(tracker_name) {
      const result = await axios
        .get("export/" + tracker_name + "/logpdf", {
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
        this.pdfurl = downloadUrl;
        const link = document.createElement("a");
        link.href = this.pdfurl;

        link.setAttribute(
          "download",
          this.username + "_" + tracker_name + "_AllLogs" + ".pdf"
        );
        document.body.appendChild(link);
        link.click();
        link.remove();
      }
    },
    logout() {
      localStorage.removeItem("token");
      this.$router.push("login");
    },
    handleupdateform(log) {
      this.upnote = log.note;
      this.upvalue = log.value;
      this.uptimestamp = log.timestamp;
      this.uplogid = log.id;
    },
    async addlog() {
      let result = await axios
        .post(
          this.cur_tracker.name + "/log",
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

        this.value = "";
        this.note = "";
      } else {
        alert("tracker not added!!! something wrong");
      }
    },
    async updatelog(id) {
      let result = await axios
        .post(
          "updatelog/" + this.cur_tracker.name + "/" + id,
          {
            value: this.upvalue,
            note: this.upnote,
            timestamp: this.uptimestamp,
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
        alert("log updated");
      }
    },
    async deletelog(id) {
      let result = await axios
        .delete(
          "deletelog/" + this.cur_tracker.name + "/" + id,

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
    async deletealllogs() {
      let result = await axios
        .delete(
          this.cur_tracker.name + "/delalllogs",

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
        alert("All Logs deleted");
      }
    },
  },

  async created() {
    const route = useRoute();
    this.tracker_id = route.params.data;

    const result = await axios
      .get("user", {
        headers: {
          "x-access-token": localStorage.getItem("token"),
        },
      })
      .catch((error) => {
        // handle this error here
        alert("Time Out");
      });
    if (result.status == 200) {
      this.username = result.data.user.name;
      console.log(result);
      console.log(this.username);
    }

    const ctracker = await axios.get("tracker/" + this.tracker_id, {
      headers: {
        "x-access-token": localStorage.getItem("token"),
      },
    });
    if (ctracker.status == 200) {
      this.cur_tracker = ctracker.data;
      console.log(ctracker.data);
    }
    const logs = await axios.get(this.cur_tracker.name + "/alllog", {
      headers: {
        "x-access-token": localStorage.getItem("token"),
      },
    });
    if (logs.status == 200) {
      this.logs = logs.data.logs;
      console.log(logs.data.logs);
      
    }
    const chart = await axios
      .get(this.cur_tracker.name + "/plot", {
        headers: {
          "x-access-token": localStorage.getItem("token"),
        },
      })
      .catch((error) => {
        // handle this error here
        alert("no plot");
      });
    if (chart.status == 200) {
      console.log(chart.data.url);
      console.log("abc");
      this.plot_url = "data:image/png;base64, " + chart.data.url;
      console.log(this.plot_url);
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
          ><h4>Hi, {{ this.username }}</h4></router-link
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
          <li class="nav-item">
            <router-link :to="{ name: 'Home' }"
              ><button type="button" class="btn btn-primary">
                Home
              </button></router-link
            >
          </li>
        </ul>
        <router-link :to="{ name: 'Welcome' }"
          ><button type="button" class="btn btn-danger" @click="logout">
            Log Out
          </button></router-link
        >
      </div>
    </div>
  </nav>
  <div class="container">
    <div class="d-grid gap-2">
      <br />

      <div
        class="card text-center"
        v-if="this.cur_tracker.trackertype != 'Multiple'"
      >
        <div class="card-header">Your Record</div>
        <div class="card-body">
          <img
            class="img-fluid"
            v-bind:src="this.plot_url"
            v-if="this.plot_url.length > 0"
            alt="Graph Will Appear Here"
          />
        </div>
        <div class="card-footer text-muted"></div>
      </div>
      <br />

      <button
        class="btn btn-primary"
        type="button"
        data-bs-toggle="modal"
        data-bs-target="#exampleModaladdlog"
      >
        <h2>Log now</h2>
      </button>
      <br />
      <br />
      <br />
    </div>
    <label
      ><h2 style="color: white">
        Your Logs on Tracker: {{ this.cur_tracker.name }}
      </h2>
      <h6 style="color: white">
        Last Tracked at: {{ this.cur_tracker.lastused }}
      </h6>
    </label>
    <button
      type="button"
      class="btn btn-secondary"
      data-bs-toggle="modal"
      data-bs-target="#exampleModalexport"
      style="float: right"
    >
      Export Data
    </button>
    <br />

    <table class="table table-dark table-hover" v-if="logs.length > 0">
      <thead>
        <tr>
          <th scope="col">SNo.</th>
          <th scope="col">Value</th>
          <th scope="col">Note</th>
          <th scope="col">Time</th>
          <th scope="col">Settings</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(log, index) in logs" :key="log.id">
          <th scope="row">{{ index }}</th>
          <td>{{ log.value }}</td>

          <td>{{ log.note }}</td>
          <td>{{ log.timestamp }}</td>
          <td>
            <div
              class="btn-group"
              role="group"
              aria-label="Basic mixed styles example"
            >
              <button
                type="button"
                class="btn btn-warning"
                data-bs-toggle="modal"
                data-bs-target="#exampleModal"
                @click="handleupdateform(log)"
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
                @click="deletelog(log.id)"
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
    <div class="d-grid gap-2" v-if="logs.length > 0">
      <button class="btn btn-danger" type="button" @click="deletealllogs">
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
        &nbsp;Delete All Logs
      </button>
      <br />
      <br />
      <br />
      <br />
    </div>

    <div class="alert alert-danger" role="alert" v-if="logs.length == 0">
      No Logs Found!!!!!!! Log now.
    </div>
  </div>

  <!-- Modal update log -->
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
                >Value (Type: {{ this.cur_tracker.trackertype }})</label
              >
              <input
                type="number"
                class="form-control"
                id="exampleInputEmail1"
                aria-describedby="emailHelp"
                v-model="upvalue"
                v-if="this.cur_tracker.trackertype == 'Numerical'"
              />
              <input
                type="value"
                class="form-control"
                id="exampleInput"
                aria-describedby="Help"
                v-model="upvalue"
                v-if="uptrackertype == 'Multiple'"
                placeholder="Separate values with comma(',')"
              />
              <input
                type="number"
                class="form-control"
                id="exampleInputEmail1"
                aria-describedby="emailHelp"
                v-model="upvalue"
                v-if="this.cur_tracker.trackertype == 'Time Duration'"
                placeholder="Give duration in minutes"
              />
              <select
                class="form-select"
                aria-label="Default select example"
                v-model="upvalue"
                v-if="this.cur_tracker.trackertype == 'Boolean'"
              >
                <option selected>Choose from Below</option>
                <option value="Yes">Yes</option>
                <option value="No">No</option>
              </select>
            </div>
            <div class="mb-3">
              <label for="exampleInputEmail1" class="form-label">Note</label>
              <input
                type="text"
                class="form-control"
                id="exampleInputEmail1"
                aria-describedby="emailHelp"
                v-model="upnote"
              />
            </div>
            <div class="mb-3">
              <label for="exampleInputPassword1" class="form-label"
                >Timestamp</label
              >
              <input
                type="datetime"
                class="form-control"
                id="exampleInputPassword1"
                v-model="uptimestamp"
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
            @click="updatelog(uplogid)"
          >
            Save
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
            Log to {{ this.cur_tracker.name }}
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
                >Value (Type: {{ this.cur_tracker.trackertype }})</label
              >
              <input
                type="number"
                class="form-control"
                id="exampleInputEmail1"
                aria-describedby="emailHelp"
                v-model="value"
                v-if="this.cur_tracker.trackertype == 'Numerical'"
              />
              <input
                type="number"
                class="form-control"
                id="exampleInputEmail1"
                aria-describedby="emailHelp"
                v-model="value"
                v-if="this.cur_tracker.trackertype == 'Time Duration'"
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
                v-if="this.cur_tracker.trackertype == 'Boolean'"
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
          <button type="button" class="btn btn-primary" @click="addlog()">
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
            <button
              class="btn btn-info"
              type="button"
              @click="getlogpdf(this.cur_tracker.name)"
            >
              Export As .pdf
            </button>
            <button
              class="btn btn-info"
              type="button"
              @click="getlogcsv(this.cur_tracker.name)"
            >
              Export As .csv
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
tr {
  text-decoration-color: antiquewhite;
}
</style>