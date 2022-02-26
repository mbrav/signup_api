import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import axios from "axios";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.bundle";

axios.defaults.withCredentials = true;
axios.defaults.baseURL = "http://localhost:8000/api"; // the FastAPI backend

const app = createApp(App);
app.use(router);
app.mount("#app");
