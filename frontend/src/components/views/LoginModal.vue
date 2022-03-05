<template>
	<div class="about-header p-3 pb-md-4 mx-auto text-center">
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
							<div class="form-floating mb-4">
								<input
									type="text"
									class="form-control"
									id="formUsername"
									v-model="form.username"
									placeholder="Username"
								/>
								<label for="formUsername">Username</label>
							</div>
							<div class="form-floating mb-4">
								<input
									type="text"
									class="form-control"
									id="formPassword"
									v-model="form.password"
									placeholder="Password"
								/>
								<label for="formPassword">Password</label>
							</div>
						</form>
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
							v-on:click="userLogin()"
						>
							Login
						</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import store from "@/store";

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
		async userLogin() {
			this.response = await store.dispatch("userLogin", this.form);
		},
	},
};
</script>

<style lang="scss"></style>
