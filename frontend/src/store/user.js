import axios from "axios";

const state = {
	isAuthenticated: false,
	token: "",
	user: null,
};

const getters = {
	isAuthenticated: (state) => !!state.user,
	stateUser: (state) => state.user,
};

const actions = {
	async userLogin({ commit, dispatch }, form) {
		await axios
			.post("/auth/token", new URLSearchParams(form))
			.then((res) => {
				this.response = res.data;
				commit("setToken", res.data.access_token);
				console.log(res.data);
				// dispatch("viewMe");
			})
			.catch((error) => {
				console.error(error);
			});
	},
	// async logIn({ dispatch }, user) {
	// 	await axios.post("login", user);
	// 	await dispatch("viewMe");
	// },
	async viewMe({ commit }) {
		let data = await axios.get("/users/me");
		await commit("setUser", data);
	},
	async logOut({ commit }) {
		let user = null;
		commit("logout", user);
	},
};

const mutations = {
	initializeStore(state) {
		if (localStorage.getItem("token")) {
			state.token = localStorage.getItem("token");
			state.isAuthenticated = true;
		} else {
			state.token = "";
			state.isAuthenticated = false;
		}
	},
	setToken(state, token) {
		state.token = token;
		state.isAuthenticated = true;
		localStorage.setItem("token", token);
	},
	setUser(state, username) {
		state.user = username;
	},
};

export default {
	state,
	getters,
	actions,
	mutations,
};
