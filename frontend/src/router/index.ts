import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      redirect: "/dashboard",
    },
    {
      path: "/login",
      component: () => import("@/views/LoginView.vue"),
      meta: { guest: true },
    },
    {
      path: "/register",
      component: () => import("@/views/RegisterView.vue"),
      meta: { guest: true },
    },
    {
      path: "/dashboard",
      component: () => import("@/views/DashboardView.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/notes",
      component: () => import("@/views/NotesView.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/tasks",
      component: () => import("@/views/TasksView.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/bookmarks",
      component: () => import("@/views/BookmarksView.vue"),
      meta: { requiresAuth: true },
    },
  ],
});

router.beforeEach((to) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { path: "/login" };
  }

  if (to.meta.guest && authStore.isAuthenticated) {
    return { path: "/dashboard" };
  }
});

export default router;
