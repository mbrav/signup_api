<template>
	<!-- VIEWS CONTROLED BY ROUTER -->
	<div class="container py-3">
		<the-header></the-header>

		<main role="main">
			<router-view />
		</main>
		<the-footer></the-footer>
	</div>
</template>

<style type="scss">
body {
	margin: 0;
}
</style>

<script>
import TheHeader from "@/components/layout/TheHeader.vue";
import TheFooter from "@/components/layout/TheFooter.vue";

export default {
	name: "App",
	components: {
		TheHeader,
		TheFooter,
	},
};
</script>
