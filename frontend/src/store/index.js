import { createStore } from "vuex";
import user from "./user";
import signup from "./signup";

export default new createStore({
	modules: { user, signup },
});
