<template>
	<header>
		<!-- NAVBAR -->
		<div
			class="d-flex flex-column flex-md-row align-items-center pb-3 mb-4 border-bottom"
		>
			<router-link to="/" class="navbar-brand">
				<img
					id="logo"
					class="d-inline-block align-top"
					src="../../assets/logo.png"
					width="46"
					height="46"
					alt="logo"
					loading="lazy"
				/>
			</router-link>
			<span class="fs-4">Signup API</span>

			<nav class="d-inline-flex mt-2 mt-md-0 ms-md-auto">
				<router-link
					to="/signups"
					class="me-3 py-2 text-dark text-decoration-none"
					>Signups</router-link
				>
				<router-link to="/" class="py-2 text-dark text-decoration-none"
					>Home</router-link
				>
			</nav>
		</div>
	</header>
</template>
