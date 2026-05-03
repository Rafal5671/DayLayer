<template>
  <div class="flex h-screen bg-gray-50 overflow-hidden">
    <aside class="w-56 bg-white border-r border-gray-100 flex flex-col shrink-0">
      <div class="px-5 py-6 text-lg font-medium text-gray-900">
        Day<span class="text-purple-600">layer</span>
      </div>

      <nav class="flex flex-col flex-1">
        <span class="px-5 py-2 text-xs uppercase tracking-wider text-gray-400">Menu</span>

        <RouterLink
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="flex items-center gap-3 px-5 py-2.5 text-sm text-gray-500 border-l-2 border-transparent hover:text-gray-900 hover:bg-gray-50 transition-colors"
          active-class="text-purple-600 bg-purple-50 border-l-purple-600 font-medium"
        >
          <component :is="item.icon" class="w-4 h-4" />
          {{ item.label }}
        </RouterLink>

        <span class="px-5 py-2 mt-4 text-xs uppercase tracking-wider text-gray-400">Account</span>

        <RouterLink
          to="/settings"
          class="flex items-center gap-3 px-5 py-2.5 text-sm text-gray-500 border-l-2 border-transparent hover:text-gray-900 hover:bg-gray-50 transition-colors"
          active-class="text-purple-600 bg-purple-50 border-l-purple-600 font-medium"
        >
          Settings
        </RouterLink>

        <div class="mt-auto px-5 py-4 flex items-center gap-3 border-t border-gray-100">
          <div
            class="w-8 h-8 rounded-full bg-purple-50 flex items-center justify-center text-xs font-medium text-purple-600"
          >
            {{ userInitials }}
          </div>
          <span class="text-sm text-gray-700">{{ authStore.user?.username }}</span>
          <button
            class="ml-auto text-gray-400 hover:text-gray-600 transition-colors"
            @click="authStore.logout()"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="w-4 h-4"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
              <polyline points="16 17 21 12 16 7" />
              <line x1="21" y1="12" x2="9" y2="12" />
            </svg>
          </button>
        </div>
      </nav>
    </aside>

    <main class="flex-1 overflow-y-auto">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { RouterLink } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();

const navItems = [
  { path: "/dashboard", label: "Dashboard", icon: "svg-dashboard" },
  { path: "/notes", label: "Notes", icon: "svg-notes" },
  { path: "/tasks", label: "Tasks", icon: "svg-tasks" },
  { path: "/bookmarks", label: "Bookmarks", icon: "svg-bookmarks" },
];

const userInitials = computed(() => {
  const username = authStore.user?.username || "";
  return username.slice(0, 2).toUpperCase();
});
</script>
