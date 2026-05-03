import { defineStore } from "pinia";
import { ref, computed } from "vue";
import api from "@/api/axios";

interface User {
  id: number;
  username: string;
  email: string;
}

export const useAuthStore = defineStore("auth", () => {
  const user = ref<User | null>(null);
  const accessToken = ref<string | null>(localStorage.getItem("access_token"));
  const refreshToken = ref<string | null>(localStorage.getItem("refresh_token"));

  const isAuthenticated = computed(() => !!accessToken.value);

  async function login(username: string, password: string) {
    const { data } = await api.post("/users/login/", { username, password });
    accessToken.value = data.access;
    refreshToken.value = data.refresh;
    localStorage.setItem("access_token", data.access);
    localStorage.setItem("refresh_token", data.refresh);
    await fetchUser();
  }

  async function register(username: string, email: string, password: string) {
    await api.post("/users/register/", { username, email, password });
    await login(username, password);
  }

  async function fetchUser() {
    const { data } = await api.get("/users/me/");
    user.value = data;
  }

  function logout() {
    user.value = null;
    accessToken.value = null;
    refreshToken.value = null;
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  }

  return {
    user,
    isAuthenticated,
    login,
    register,
    fetchUser,
    logout,
  };
});
