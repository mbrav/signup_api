import axios from "axios";

const state = {
	signups: null,
	signup: null,
};

const getters = {
	signups: (state) => state.signups,
	signup: (state) => state.signup,
};

const actions = {
	async getSignups({ commit }) {
		await axios
			.get("/signups")
			.then((res) => {
				commit("setSignups", res.data.items);
			})
			.catch((error) => {
				console.error(error);
			});
	},
	async createSignup({ commit }, form) {
		axios
			.post("/signups", form)
			.then((res) => {
				this.response = res.data;
				commit("setSignup", res.data);
				console.log(res);
			})
			.catch((error) => {
				console.error(error);
			});
	},
};

const mutations = {
	setSignup(state, item) {
		state.signup = item;
	},
	setSignups(state, items) {
		state.signups = items;
	},
};

export default {
	state,
	getters,
	actions,
	mutations,
};
