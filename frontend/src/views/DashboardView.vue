<template>
  <AppLayout>
    <div class="p-8">
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-xl font-medium text-gray-900">
            Good {{ timeOfDay }}, {{ authStore.user?.username }}
          </h1>
          <p class="text-sm text-gray-400 mt-1">{{ currentDate }}</p>
        </div>
      </div>

      <div class="grid grid-cols-3 gap-4 mb-8">
        <div class="bg-gray-50 rounded-xl p-5">
          <p class="text-xs text-gray-400 mb-2">Notes</p>
          <p class="text-2xl font-medium text-gray-900">{{ notes.length }}</p>
          <p class="text-xs text-gray-400 mt-1">total saved</p>
        </div>
        <div class="bg-gray-50 rounded-xl p-5">
          <p class="text-xs text-gray-400 mb-2">Tasks</p>
          <p class="text-2xl font-medium text-gray-900">{{ pendingTasks.length }}</p>
          <p class="text-xs text-gray-400 mt-1">pending</p>
        </div>
        <div class="bg-gray-50 rounded-xl p-5">
          <p class="text-xs text-gray-400 mb-2">Bookmarks</p>
          <p class="text-2xl font-medium text-gray-900">{{ bookmarks.length }}</p>
          <p class="text-xs text-gray-400 mt-1">total saved</p>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div class="bg-white border border-gray-100 rounded-xl p-5">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-sm font-medium text-gray-900">Tasks due today</h2>
            <RouterLink to="/tasks" class="text-xs text-purple-600 hover:underline"
              >View all</RouterLink
            >
          </div>
          <div v-if="todayTasks.length === 0" class="text-sm text-gray-400">
            No tasks due today.
          </div>
          <div
            v-for="task in todayTasks"
            :key="task.id"
            class="flex items-center gap-3 py-2.5 border-b border-gray-50 last:border-0"
          >
            <div
              class="w-4 h-4 rounded border shrink-0 flex items-center justify-center"
              :class="
                task.status === 'done' ? 'bg-purple-600 border-purple-600' : 'border-gray-300'
              "
            >
              <svg
                v-if="task.status === 'done'"
                class="w-2.5 h-2.5 text-white"
                viewBox="0 0 10 8"
                fill="none"
              >
                <path
                  d="M1 4l3 3 5-6"
                  stroke="currentColor"
                  stroke-width="1.5"
                  stroke-linecap="round"
                />
              </svg>
            </div>
            <span
              class="text-sm text-gray-700 flex-1"
              :class="{ 'line-through text-gray-400': task.status === 'done' }"
            >
              {{ task.title }}
            </span>
            <span
              class="text-xs px-2 py-0.5 rounded font-medium"
              :class="{
                'bg-red-50 text-red-700': task.priority === 'high',
                'bg-amber-50 text-amber-700': task.priority === 'medium',
                'bg-green-50 text-green-700': task.priority === 'low',
              }"
            >
              {{ task.priority }}
            </span>
          </div>
        </div>

        <div class="bg-white border border-gray-100 rounded-xl p-5">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-sm font-medium text-gray-900">Recent notes</h2>
            <RouterLink to="/notes" class="text-xs text-purple-600 hover:underline"
              >View all</RouterLink
            >
          </div>
          <div v-if="notes.length === 0" class="text-sm text-gray-400">No notes yet.</div>
          <div
            v-for="note in recentNotes"
            :key="note.id"
            class="py-2.5 border-b border-gray-50 last:border-0"
          >
            <p class="text-sm font-medium text-gray-800">{{ note.title }}</p>
            <p class="text-xs text-gray-400 mt-0.5">{{ formatDate(note.updated_at) }}</p>
          </div>
        </div>

        <div class="bg-white border border-gray-100 rounded-xl p-5 col-span-2">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-sm font-medium text-gray-900">Recent bookmarks</h2>
            <RouterLink to="/bookmarks" class="text-xs text-purple-600 hover:underline"
              >View all</RouterLink
            >
          </div>
          <div v-if="bookmarks.length === 0" class="text-sm text-gray-400">No bookmarks yet.</div>
          <div class="grid grid-cols-2 gap-x-8">
            <div
              v-for="bookmark in recentBookmarks"
              :key="bookmark.id"
              class="flex items-center gap-3 py-2.5 border-b border-gray-50 last:border-0"
            >
              <div class="w-7 h-7 rounded-lg bg-gray-50 flex items-center justify-center shrink-0">
                <svg
                  class="w-3.5 h-3.5 text-gray-400"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" />
                  <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" />
                </svg>
              </div>
              <div class="min-w-0">
                <p class="text-sm text-gray-800 truncate">{{ bookmark.title || bookmark.url }}</p>
                <p class="text-xs text-gray-400 truncate">{{ bookmark.url }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { RouterLink } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import AppLayout from "@/components/layout/AppLayout.vue";
import api from "@/api/axios";
import type { Note, Task, Bookmark } from "@/types";

const authStore = useAuthStore();

const notes = ref<Note[]>([]);
const tasks = ref<Task[]>([]);
const bookmarks = ref<Bookmark[]>([]);

const today = new Date().toISOString().split("T")[0];

const pendingTasks = computed(() => tasks.value.filter((t) => t.status !== "done"));

const todayTasks = computed(() => tasks.value.filter((t) => t.deadline === today));

const recentNotes = computed(() => notes.value.slice(0, 3));
const recentBookmarks = computed(() => bookmarks.value.slice(0, 4));

const timeOfDay = computed(() => {
  const hour = new Date().getHours();
  if (hour < 12) return "morning";
  if (hour < 18) return "afternoon";
  return "evening";
});

const currentDate = computed(() =>
  new Date().toLocaleDateString("en-GB", {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
  }),
);

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString("en-GB", {
    day: "numeric",
    month: "short",
  });
}

onMounted(async () => {
  const [notesRes, tasksRes, bookmarksRes] = await Promise.all([
    api.get("/notes/"),
    api.get("/tasks/"),
    api.get("/bookmarks/"),
  ]);
  notes.value = notesRes.data.results ?? notesRes.data;
  tasks.value = tasksRes.data.results ?? tasksRes.data;
  bookmarks.value = bookmarksRes.data.results ?? bookmarksRes.data;
});
</script>
