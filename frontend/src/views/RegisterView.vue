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
        <form @submit.prevent="handleRegister" novalidate>
          <div class="mb-4">
            <label class="block text-sm text-gray-600 mb-1.5">Username</label>
            <input
              v-model="form.username"
              type="text"
              placeholder="your username"
              class="w-full px-3 py-2 text-sm border rounded-lg outline-none transition-colors"
              :class="
                errors.username
                  ? 'border-red-300 focus:border-red-400'
                  : 'border-gray-200 focus:border-purple-400'
              "
              @blur="validateUsername"
            />
            <p v-if="errors.username" class="text-xs text-red-500 mt-1">{{ errors.username }}</p>
          </div>

          <div class="mb-4">
            <label class="block text-sm text-gray-600 mb-1.5">Email</label>
            <input
              v-model="form.email"
              type="email"
              placeholder="you@example.com"
              class="w-full px-3 py-2 text-sm border rounded-lg outline-none transition-colors"
              :class="
                errors.email
                  ? 'border-red-300 focus:border-red-400'
                  : 'border-gray-200 focus:border-purple-400'
              "
              @blur="validateEmail"
            />
            <p v-if="errors.email" class="text-xs text-red-500 mt-1">{{ errors.email }}</p>
          </div>

          <div class="mb-4">
            <label class="block text-sm text-gray-600 mb-1.5">Password</label>
            <input
              v-model="form.password"
              type="password"
              placeholder="min. 8 characters"
              class="w-full px-3 py-2 text-sm border rounded-lg outline-none transition-colors"
              :class="
                errors.password
                  ? 'border-red-300 focus:border-red-400'
                  : 'border-gray-200 focus:border-purple-400'
              "
              @blur="validatePassword"
            />
            <p v-if="errors.password" class="text-xs text-red-500 mt-1">{{ errors.password }}</p>
          </div>

          <div class="mb-6">
            <label class="block text-sm text-gray-600 mb-1.5">Confirm password</label>
            <input
              v-model="form.confirmPassword"
              type="password"
              placeholder="repeat your password"
              class="w-full px-3 py-2 text-sm border rounded-lg outline-none transition-colors"
              :class="
                errors.confirmPassword
                  ? 'border-red-300 focus:border-red-400'
                  : 'border-gray-200 focus:border-purple-400'
              "
              @blur="validateConfirmPassword"
            />
            <p v-if="errors.confirmPassword" class="text-xs text-red-500 mt-1">
              {{ errors.confirmPassword }}
            </p>
          </div>

          <p v-if="error" class="text-sm text-red-500 mb-4">{{ error }}</p>

          <button
            type="submit"
            :disabled="loading || !isFormValid"
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
import { ref, computed } from "vue";
import { useRouter, RouterLink } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const authStore = useAuthStore();

const form = ref({
  username: "",
  email: "",
  password: "",
  confirmPassword: "",
});

const errors = ref({
  username: "",
  email: "",
  password: "",
  confirmPassword: "",
});

const loading = ref(false);
const error = ref("");

function validateUsername() {
  if (!form.value.username) {
    errors.value.username = "Username is required";
  } else if (form.value.username.length < 3) {
    errors.value.username = "Username must be at least 3 characters";
  } else if (!/^[a-zA-Z0-9_]+$/.test(form.value.username)) {
    errors.value.username = "Username can only contain letters, numbers and underscores";
  } else {
    errors.value.username = "";
  }
}

function validateEmail() {
  if (!form.value.email) {
    errors.value.email = "Email is required";
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) {
    errors.value.email = "Enter a valid email address";
  } else {
    errors.value.email = "";
  }
}

function validatePassword() {
  if (!form.value.password) {
    errors.value.password = "Password is required";
  } else if (form.value.password.length < 8) {
    errors.value.password = "Password must be at least 8 characters";
  } else if (!/[A-Z]/.test(form.value.password)) {
    errors.value.password = "Password must contain at least one uppercase letter";
  } else if (!/[0-9]/.test(form.value.password)) {
    errors.value.password = "Password must contain at least one number";
  } else {
    errors.value.password = "";
  }
}

function validateConfirmPassword() {
  if (!form.value.confirmPassword) {
    errors.value.confirmPassword = "Please confirm your password";
  } else if (form.value.confirmPassword !== form.value.password) {
    errors.value.confirmPassword = "Passwords do not match";
  } else {
    errors.value.confirmPassword = "";
  }
}

function validateAll() {
  validateUsername();
  validateEmail();
  validatePassword();
  validateConfirmPassword();
}

const isFormValid = computed(
  () =>
    form.value.username &&
    form.value.email &&
    form.value.password &&
    form.value.confirmPassword &&
    !errors.value.username &&
    !errors.value.email &&
    !errors.value.password &&
    !errors.value.confirmPassword,
);

async function handleRegister() {
  validateAll();
  if (!isFormValid.value) return;

  loading.value = true;
  error.value = "";
  try {
    await authStore.register(form.value.username, form.value.email, form.value.password);
    router.push("/dashboard");
  } catch {
    error.value = "Registration failed. Username may already be taken.";
  } finally {
    loading.value = false;
  }
}
</script>
