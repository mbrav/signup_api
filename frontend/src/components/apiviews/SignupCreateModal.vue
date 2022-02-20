<template>
	<div class="about-header p-3 pb-md-4 mx-auto text-center">
		<button
			type="button"
			class="btn btn-success btn-lg"
			data-bs-toggle="modal"
			data-bs-target="#signupModal"
		>
			New Signup
		</button>
		<div
			class="modal fade"
			id="signupModal"
			tabindex="-1"
			aria-labelledby="signupModalLabel"
			aria-hidden="true"
		>
			<div class="modal-dialog">
				<div class="modal-content">
					<div class="modal-header">
						<h5 class="modal-title" id="signupModalLabel">
							New Signup
						</h5>
						<button
							type="button"
							class="btn-close"
							data-bs-dismiss="modal"
							aria-label="Close"
						></button>
					</div>
					<div class="modal-body">
						<form>
							<div class="form-floating mb-4">
								<input
									type="text"
									class="form-control"
									id="formFirstName"
									v-model="form.first_name"
									placeholder="name@example.com"
								/>
								<label for="formFirstName">First Name</label>
							</div>
							<div class="form-floating mb-4">
								<input
									type="text"
									class="form-control"
									id="formLastName"
									v-model="form.last_name"
									placeholder="Last Name"
								/>
								<label for="formLastName">Last Name</label>
							</div>
							<div class="form-floating mb-4">
								<input
									type="text"
									class="form-control"
									id="formPhone"
									v-model="form.phone"
									placeholder="Phone"
								/>
								<label for="formPhone">Phone</label>
							</div>
							<div class="form-floating mb-4">
								<input
									type="text"
									class="form-control"
									id="formEmail"
									v-model="form.email"
									placeholder="Email"
								/>
								<label for="formPhone">Email</label>
							</div>
							<div class="form-floating mb-4">
								<input
									type="text"
									class="form-control"
									id="formClass"
									v-model="form.class_id"
									placeholder="Email"
								/>
								<label for="formPhone">Class</label>
							</div>
						</form>
					</div>
					<div class="alert alert-success" role="alert">
						A simple success alert—check it out!
					</div>
					<div class="modal-footer">
						<button
							type="button"
							class="btn btn-secondary"
							data-bs-dismiss="modal"
						>
							Close
						</button>
						<button
							type="button"
							class="btn btn-primary"
							v-on:click="createSignup()"
						>
							Signup
						</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import axios from "axios";

export default {
	name: "SignupCreateModal",
	data() {
		return {
			form: {
				first_name: "",
				last_name: "",
				phone: "",
				email: "",
				class_id: "",
			},
			response: {},
		};
	},
	methods: {
		createSignup() {
			axios
				.post("/signup", this.form)
				.then((res) => {
					this.response = res.data;
					console.error(res);
				})
				.catch((error) => {
					console.error(error);
				});
		},
	},
	created() {
		// this.createSignup();
	},
};
</script>
