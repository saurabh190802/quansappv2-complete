import { createApp } from "vue";
import App from "./App.vue";
import './axios'
import "./assets/main.css";
import "bootstrap/dist/css/bootstrap.css";
import bootstrap from "bootstrap/dist/js/bootstrap.bundle.js";
import router from "./router";
import vue3GoogleLogin from "vue3-google-login";

createApp(App)
  .use(bootstrap)
  .use(router)
  .use(vue3GoogleLogin, {
    clientId:
      "908340866608-8d3fd694859m5klg073q8l16f0ba2skm.apps.googleusercontent.com",
    clientSecret: "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",
  })
  .mount("#app");

