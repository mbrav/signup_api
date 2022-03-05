import { createRouter, createWebHistory } from "vue-router";
// import store from "@/store";

const routes = [
	{
		path: "/",
		name: "home",
		component: () =>
			import(/* webpackChunkName: "home" */ "../views/HomeView.vue"),
	},
	{
		path: "/signups",
		name: "signups",
		meta: {
			requireLogin: true,
		},
		// route level code-splitting
		// this generates a separate chunk (about.[hash].js) for this route
		// which is lazy-loaded when the route is visited.
		component: () =>
			import(/* webpackChunkName: "signups" */ "../views/SignupView.vue"),
	},
];

const router = createRouter({
	history: createWebHistory(process.env.BASE_URL),
	routes: routes,
});

// router.beforeEach((to, from, next) => {
// 	if (
// 		to.matched.some((record) => record.meta.requireLogin) &&
// 		!store.state.isAuthenticated
// 	) {
// 		next({ name: "home", query: { to: to.path } });
// 		console.log(store.state);
// 	} else {
// 		next();
// 	}
// });

export default router;
