<template>
	<div class="about-header p-3 pb-md-4 mx-auto text-center">
		<button
			type="button"
			class="btn btn-success btn-lg"
			data-bs-toggle="modal"
			data-bs-target="#loginModal"
		>
			New Signup
		</button>
		<div
			class="modal fade"
			id="loginModal"
			tabindex="-1"
			aria-labelledby="loginModalLabel"
			aria-hidden="true"
		>
			<div class="modal-dialog">
				<div class="modal-content">
					<div class="modal-header">
						<h5 class="modal-title" id="loginModalLabel">Login</h5>
						<button
							type="button"
							class="btn-close"
							data-bs-dismiss="modal"
							aria-label="Close"
						></button>
					</div>
					<div class="modal-body">
						<form>
							<div class="mb-3">
								<label for="formUsername" class="form-label"
									>Username</label
								>
								<input
									type="email"
									class="form-control"
									id="formUsername"
									aria-describedby="usernameHelp"
								/>
								<div id="usernameHelp" class="form-text">
									We'll never share your username with anyone
									else.
								</div>
							</div>
							<div class="mb-3">
								<label for="formPassword" class="form-label"
									>Password</label
								>
								<input
									type="password"
									class="form-control"
									id="formPassword"
									aria-describedby="passwordHelp"
								/>
								<div id="passwordHelp" class="form-text">
									Are passwords are hashed with the most
									secure algorithm
									<a
										href="https://github.com/p-h-c/phc-winner-argon2"
										>argon2</a
									>
								</div>
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
							v-on:click="authenticateToken()"
						>
							Authenticate
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
	name: "LoginModal",
	data() {
		return {
			form: {
				username: "",
				password: "",
			},
			response: {},
		};
	},
	methods: {
		authenticateToken() {
			axios
				.post("users/token", this.form)
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
