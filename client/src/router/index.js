import { createRouter, createWebHistory } from "vue-router";
import Welcome from "../views/Welcome.vue";
import Login from "../views/Login.vue"
import Signup from "../views/Signup.vue";
import Home from "../views/Home.vue";
import TrackerDashboard from "../views/TrackerDashboard.vue";
import Profile from "../views/Profile.vue";
import Resetpwd from "../views/Resetpwd.vue"

const routes = [
  {
    path: "/",
    name: "Welcome",
    component: Welcome,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/signup",
    name: "Signup",
    component: Signup,
  },
  {
    path: "/Home",
    name: "Home",
    component: Home,
    props: true,
  },
  {
    path: "/TrackerDashboard/:data",
    name: "TrackerDashboard",
    component: TrackerDashboard,
    props: true,
  },
  {
    path: "/profile",
    name: "Profile",
    component: Profile,
    props: true,
  },
  {
    path: "/rpwd",
    name: "Resetpwd",
    component: Resetpwd,
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
