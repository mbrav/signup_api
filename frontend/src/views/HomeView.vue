<template>
	<div class="home">
		<HealthCheck msg="Welcome to Signup API" />
	</div>
</template>

<script>
// @ is an alias to /src
import HealthCheck from "@/components/views/HealthCheck.vue";

export default {
	name: "HomeView",
	components: {
		HealthCheck,
	},
};
</script>
