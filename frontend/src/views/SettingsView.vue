<template>
  <AppLayout>
    <div class="p-8 max-w-2xl">
      <h1 class="text-xl font-medium text-gray-900 mb-8">Settings</h1>

      <div class="space-y-6">
        <div class="bg-white border border-gray-100 rounded-xl p-6">
          <h2 class="text-sm font-medium text-gray-900 mb-5">Profile</h2>

          <div class="mb-4">
            <label class="block text-xs text-gray-400 mb-1.5">Username</label>
            <input
              v-model="profileForm.username"
              type="text"
              class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg outline-none focus:border-purple-400 transition-colors"
            />
            <p v-if="profileErrors.username" class="text-xs text-red-500 mt-1">
              {{ profileErrors.username }}
            </p>
          </div>

          <div class="mb-6">
            <label class="block text-xs text-gray-400 mb-1.5">Email</label>
            <input
              v-model="profileForm.email"
              type="email"
              class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg outline-none focus:border-purple-400 transition-colors"
            />
            <p v-if="profileErrors.email" class="text-xs text-red-500 mt-1">
              {{ profileErrors.email }}
            </p>
          </div>

          <div class="flex items-center justify-between">
            <p v-if="profileSuccess" class="text-xs text-green-600">Profile updated successfully</p>
            <div class="ml-auto">
              <button
                @click="saveProfile"
                :disabled="profileLoading"
                class="px-4 py-2 text-sm font-medium text-white bg-purple-600 rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50"
              >
                {{ profileLoading ? "Saving..." : "Save changes" }}
              </button>
            </div>
          </div>
        </div>

        <div class="bg-white border border-gray-100 rounded-xl p-6">
          <h2 class="text-sm font-medium text-gray-900 mb-5">Password</h2>

          <div class="mb-4">
            <label class="block text-xs text-gray-400 mb-1.5">Current password</label>
            <input
              v-model="passwordForm.currentPassword"
              type="password"
              placeholder="••••••••"
              class="w-full px-3 py-2 text-sm border rounded-lg outline-none transition-colors"
              :class="
                passwordErrors.currentPassword
                  ? 'border-red-300 focus:border-red-400'
                  : 'border-gray-200 focus:border-purple-400'
              "
            />
            <p v-if="passwordErrors.currentPassword" class="text-xs text-red-500 mt-1">
              {{ passwordErrors.currentPassword }}
            </p>
          </div>

          <div class="mb-4">
            <label class="block text-xs text-gray-400 mb-1.5">New password</label>
            <input
              v-model="passwordForm.newPassword"
              type="password"
              placeholder="min. 8 characters"
              class="w-full px-3 py-2 text-sm border rounded-lg outline-none transition-colors"
              :class="
                passwordErrors.newPassword
                  ? 'border-red-300 focus:border-red-400'
                  : 'border-gray-200 focus:border-purple-400'
              "
            />
            <p v-if="passwordErrors.newPassword" class="text-xs text-red-500 mt-1">
              {{ passwordErrors.newPassword }}
            </p>
          </div>

          <div class="mb-6">
            <label class="block text-xs text-gray-400 mb-1.5">Confirm new password</label>
            <input
              v-model="passwordForm.confirmPassword"
              type="password"
              placeholder="repeat new password"
              class="w-full px-3 py-2 text-sm border rounded-lg outline-none transition-colors"
              :class="
                passwordErrors.confirmPassword
                  ? 'border-red-300 focus:border-red-400'
                  : 'border-gray-200 focus:border-purple-400'
              "
            />
            <p v-if="passwordErrors.confirmPassword" class="text-xs text-red-500 mt-1">
              {{ passwordErrors.confirmPassword }}
            </p>
          </div>

          <div class="flex items-center justify-between">
            <p v-if="passwordSuccess" class="text-xs text-green-600">
              Password changed successfully
            </p>
            <p v-if="passwordErrors.general" class="text-xs text-red-500">
              {{ passwordErrors.general }}
            </p>
            <div class="ml-auto">
              <button
                @click="savePassword"
                :disabled="passwordLoading"
                class="px-4 py-2 text-sm font-medium text-white bg-purple-600 rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50"
              >
                {{ passwordLoading ? "Saving..." : "Change password" }}
              </button>
            </div>
          </div>
        </div>

        <div class="bg-white border border-red-100 rounded-xl p-6">
          <h2 class="text-sm font-medium text-gray-900 mb-2">Danger zone</h2>
          <p class="text-xs text-gray-400 mb-5">
            Once you delete your account, all your notes, tasks and bookmarks will be permanently
            removed. This action cannot be undone.
          </p>

          <button
            @click="showDeleteConfirm = true"
            class="px-4 py-2 text-sm font-medium text-red-600 border border-red-200 rounded-lg hover:bg-red-50 transition-colors"
          >
            Delete account
          </button>
        </div>
      </div>
    </div>

    <div
      v-if="showDeleteConfirm"
      class="fixed inset-0 bg-black/40 flex items-center justify-center z-50"
      @click.self="showDeleteConfirm = false"
    >
      <div class="bg-white rounded-xl w-full max-w-sm p-6">
        <h2 class="text-base font-medium text-gray-900 mb-2">Delete account</h2>
        <p class="text-sm text-gray-500 mb-6">
          Are you sure? All your data will be permanently deleted. Type your username to confirm.
        </p>

        <input
          v-model="deleteConfirmUsername"
          type="text"
          :placeholder="authStore.user?.username"
          class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg outline-none focus:border-red-400 transition-colors mb-4"
        />

        <div class="flex gap-3 justify-end">
          <button
            @click="showDeleteConfirm = false"
            class="px-4 py-2 text-sm text-gray-500 hover:text-gray-700 transition-colors"
          >
            Cancel
          </button>
          <button
            @click="deleteAccount"
            :disabled="deleteConfirmUsername !== authStore.user?.username || deleteLoading"
            class="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50"
          >
            {{ deleteLoading ? "Deleting..." : "Delete account" }}
          </button>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import AppLayout from "@/components/layout/AppLayout.vue";
import { useAuthStore } from "@/stores/auth";
import api from "@/api/axios";

const authStore = useAuthStore();

const profileForm = ref({ username: "", email: "" });
const profileErrors = ref({ username: "", email: "" });
const profileLoading = ref(false);
const profileSuccess = ref(false);

const passwordForm = ref({ currentPassword: "", newPassword: "", confirmPassword: "" });
const passwordErrors = ref({
  currentPassword: "",
  newPassword: "",
  confirmPassword: "",
  general: "",
});
const passwordLoading = ref(false);
const passwordSuccess = ref(false);

const showDeleteConfirm = ref(false);
const deleteConfirmUsername = ref("");
const deleteLoading = ref(false);

onMounted(() => {
  profileForm.value.username = authStore.user?.username || "";
  profileForm.value.email = authStore.user?.email || "";
});

function validateProfile() {
  profileErrors.value = { username: "", email: "" };
  if (!profileForm.value.username) {
    profileErrors.value.username = "Username is required";
  } else if (profileForm.value.username.length < 3) {
    profileErrors.value.username = "Username must be at least 3 characters";
  }
  if (!profileForm.value.email) {
    profileErrors.value.email = "Email is required";
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(profileForm.value.email)) {
    profileErrors.value.email = "Enter a valid email address";
  }
  return !profileErrors.value.username && !profileErrors.value.email;
}

async function saveProfile() {
  if (!validateProfile()) return;
  profileLoading.value = true;
  profileSuccess.value = false;
  try {
    await api.patch("/users/me/", {
      username: profileForm.value.username,
      email: profileForm.value.email,
    });
    await authStore.fetchUser();
    profileSuccess.value = true;
    setTimeout(() => (profileSuccess.value = false), 3000);
  } catch {
    profileErrors.value.username = "Failed to update profile. Username may already be taken.";
  } finally {
    profileLoading.value = false;
  }
}

function validatePassword() {
  passwordErrors.value = { currentPassword: "", newPassword: "", confirmPassword: "", general: "" };
  if (!passwordForm.value.currentPassword) {
    passwordErrors.value.currentPassword = "Current password is required";
  }
  if (!passwordForm.value.newPassword) {
    passwordErrors.value.newPassword = "New password is required";
  } else if (passwordForm.value.newPassword.length < 8) {
    passwordErrors.value.newPassword = "Password must be at least 8 characters";
  } else if (!/[A-Z]/.test(passwordForm.value.newPassword)) {
    passwordErrors.value.newPassword = "Password must contain at least one uppercase letter";
  } else if (!/[0-9]/.test(passwordForm.value.newPassword)) {
    passwordErrors.value.newPassword = "Password must contain at least one number";
  }
  if (!passwordForm.value.confirmPassword) {
    passwordErrors.value.confirmPassword = "Please confirm your new password";
  } else if (passwordForm.value.confirmPassword !== passwordForm.value.newPassword) {
    passwordErrors.value.confirmPassword = "Passwords do not match";
  }
  return (
    !passwordErrors.value.currentPassword &&
    !passwordErrors.value.newPassword &&
    !passwordErrors.value.confirmPassword
  );
}

async function savePassword() {
  if (!validatePassword()) return;
  passwordLoading.value = true;
  passwordSuccess.value = false;
  try {
    await api.post("/users/change-password/", {
      current_password: passwordForm.value.currentPassword,
      new_password: passwordForm.value.newPassword,
    });
    passwordForm.value = { currentPassword: "", newPassword: "", confirmPassword: "" };
    passwordSuccess.value = true;
    setTimeout(() => (passwordSuccess.value = false), 3000);
  } catch {
    passwordErrors.value.general = "Current password is incorrect";
  } finally {
    passwordLoading.value = false;
  }
}

async function deleteAccount() {
  deleteLoading.value = true;
  try {
    await api.delete("/users/me/");
    authStore.logout();
  } catch {
    showDeleteConfirm.value = false;
  } finally {
    deleteLoading.value = false;
  }
}
</script>
