<template>
	<div class="table-responsive">
		<table class="table table-borderless">
			<p class="fs-5 text-muted"></p>
			<thead>
				<tr>
					<th scope="col">#</th>
					<th scope="col">First</th>
					<th scope="col">Last</th>
					<th scope="col">Phone</th>
					<th scope="col">Email</th>
					<th scope="col">Class</th>
				</tr>
			</thead>
			<tbody>
				<tr v-for="(signup, index) in data" :key="index">
					<th scope="row">{{ signup.id }}</th>
					<th>{{ signup.first_name }}</th>
					<td>{{ signup.last_name }}</td>
					<td>{{ signup.phone }}</td>
					<td>{{ signup.email }}</td>
					<td>{{ signup.class_id }}</td>
				</tr>
			</tbody>
		</table>
	</div>
</template>

<script>
import store from "@/store";

export default {
	name: "SignupTable",
	data() {
		return {
			data: [],
		};
	},
	methods: {
		async getSignups() {
			await store.dispatch("getSignups", this.form);
			this.data = store.getters.signups;
		},
	},
	created() {
		this.getSignups();
	},
};
</script>
