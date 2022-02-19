<template>
	<!-- VIEWS CONTROLED BY ROUTER -->
	<div class="container py-3">
		<the-header></the-header>

		<main role="main">
			<router-view />
		</main>
	</div>
</template>

<style>
body {
	margin: 0;
}
</style>

<script>
import TheHeader from "@/components/layout/TheHeader.vue";

export default {
	name: "App",
	components: {
		TheHeader,
	},
};
</script>
