<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center">
    <div class="w-full max-w-sm">
      <div class="text-center mb-8">
        <h1 class="text-2xl font-medium text-gray-900">
          Day<span class="text-purple-600">layer</span>
        </h1>
        <p class="text-sm text-gray-500 mt-2">Sign in to your account</p>
      </div>

      <div class="bg-white border border-gray-100 rounded-xl p-8">
        <form @submit.prevent="handleLogin">
          <div class="mb-4">
            <label class="block text-sm text-gray-600 mb-1.5">Username</label>
            <input
              v-model="form.username"
              type="text"
              placeholder="your username"
              class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg outline-none focus:border-purple-400 transition-colors"
              required
            />
          </div>

          <div class="mb-6">
            <label class="block text-sm text-gray-600 mb-1.5">Password</label>
            <input
              v-model="form.password"
              type="password"
              placeholder="••••••••"
              class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg outline-none focus:border-purple-400 transition-colors"
              required
            />
          </div>

          <p v-if="error" class="text-sm text-red-500 mb-4">{{ error }}</p>

          <button
            type="submit"
            :disabled="loading"
            class="w-full py-2.5 text-sm font-medium text-white bg-purple-600 rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50"
          >
            {{ loading ? "Signing in..." : "Sign in" }}
          </button>
        </form>
      </div>

      <p class="text-center text-sm text-gray-500 mt-6">
        No account?
        <RouterLink to="/register" class="text-purple-600 hover:underline">Create one</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter, RouterLink } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const authStore = useAuthStore();

const form = ref({ username: "", password: "" });
const loading = ref(false);
const error = ref("");

async function handleLogin() {
  loading.value = true;
  error.value = "";
  try {
    await authStore.login(form.value.username, form.value.password);
    router.push("/dashboard");
  } catch {
    error.value = "Invalid username or password";
  } finally {
    loading.value = false;
  }
}
</script>
