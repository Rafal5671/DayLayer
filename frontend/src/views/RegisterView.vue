<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center">
    <div class="w-full max-w-sm">
      <div class="text-center mb-8">
        <h1 class="text-2xl font-medium text-gray-900">
          Day<span class="text-purple-600">layer</span>
        </h1>
        <p class="text-sm text-gray-500 mt-2">Create your account</p>
      </div>

      <div class="bg-white border border-gray-100 rounded-xl p-8">
        <form @submit.prevent="handleRegister">
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

          <div class="mb-4">
            <label class="block text-sm text-gray-600 mb-1.5">Email</label>
            <input
              v-model="form.email"
              type="email"
              placeholder="you@example.com"
              class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg outline-none focus:border-purple-400 transition-colors"
              required
            />
          </div>

          <div class="mb-6">
            <label class="block text-sm text-gray-600 mb-1.5">Password</label>
            <input
              v-model="form.password"
              type="password"
              placeholder="min. 8 characters"
              class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg outline-none focus:border-purple-400 transition-colors"
              required
              minlength="8"
            />
          </div>

          <p v-if="error" class="text-sm text-red-500 mb-4">{{ error }}</p>

          <button
            type="submit"
            :disabled="loading"
            class="w-full py-2.5 text-sm font-medium text-white bg-purple-600 rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50"
          >
            {{ loading ? "Creating account..." : "Create account" }}
          </button>
        </form>
      </div>

      <p class="text-center text-sm text-gray-500 mt-6">
        Already have an account?
        <RouterLink to="/login" class="text-purple-600 hover:underline">Sign in</RouterLink>
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

const form = ref({ username: "", email: "", password: "" });
const loading = ref(false);
const error = ref("");

async function handleRegister() {
  loading.value = true;
  error.value = "";
  try {
    await authStore.register(form.value.username, form.value.email, form.value.password);
    router.push("/dashboard");
  } catch {
    error.value = "Registration failed. Try a different username.";
  } finally {
    loading.value = false;
  }
}
</script>
