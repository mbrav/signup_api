<template>
	<div class="home">
		<StatusHeader msg="Welcome to Signup API" />
	</div>
</template>

<script>
// @ is an alias to /src
import StatusHeader from "@/components/apiviews/StatusHeader.vue";

export default {
	name: "HomeView",
	components: {
		StatusHeader,
	},
};
</script>
