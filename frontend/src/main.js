import { createApp } from "vue";
import axios from "axios";

import App from "@/App.vue";
import router from "@/router";
import store from "@/store";

axios.defaults.withCredentials = true;
axios.defaults.baseURL = "http://localhost:8000/api"; // the FastAPI backend

const app = createApp(App);
app.use(router, store);
app.mount("#app");
