<template>
	<h2 class="display-6 text-center mb-4">Signups</h2>
	<SignupCreateModal />
	<SignupTable />
</template>

<script>
// @ is an alias to /src
import SignupCreateModal from "@/components/apiviews/SignupCreateModal.vue";
import SignupTable from "@/components/apiviews/SignupTable.vue";

export default {
	name: "SignupView",
	components: {
		SignupCreateModal,
		SignupTable,
	},
};
</script>
