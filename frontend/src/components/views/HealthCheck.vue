<template>
	<div class="about-header p-3 pb-md-4 mx-auto text-center">
		<h1 class="display-4 fw-normal">HealthCheck {{ status }}</h1>
		<p class="fs-5 text-muted">"{{ message }}"</p>
		<p class="fs-5 text-muted">Server time: {{ time }}</p>
		<button
			v-on:click="getMessage()"
			type="button"
			class="btn btn-success btn-lg"
		>
			Test Response
		</button>
	</div>
</template>

<script>
import axios from "axios";

export default {
	name: "HealthCheck",
	data() {
		return {
			status: "",
			message: "",
			time: "",
			data: "",
		};
	},
	methods: {
		async getMessage() {
			await axios
				.get("/")
				.then((res) => {
					this.data = res.data;
					this.status = res.data.status;
					this.message = res.data.response;
					this.time = res.data.time;
				})
				.catch((error) => {
					console.error(error);
				});
		},
	},
	async created() {
		await this.getMessage();
	},
};
</script>
