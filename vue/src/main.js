import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import axios from "axios";

import "../node_modules/bootstrap/dist/css/bootstrap.css";
import "../node_modules/bootstrap/dist/js/bootstrap.bundle";
// import "animate.css";

axios.defaults.withCredentials = true;
axios.defaults.baseURL = "http://localhost:8000/"; // the FastAPI backend

createApp(App).use(router).mount("#app");
