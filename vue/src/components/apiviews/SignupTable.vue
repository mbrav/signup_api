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
import axios from "axios";

export default {
	name: "SignupTable",
	data() {
		return {
			data: [],
		};
	},
	methods: {
		getSignups() {
			axios
				.get("/signups")
				.then((res) => {
					this.data = res.data.items;
					console.log(res.data);
				})
				.catch((error) => {
					console.error(error);
				});
		},
	},
	created() {
		this.getSignups();
	},
};
</script>
