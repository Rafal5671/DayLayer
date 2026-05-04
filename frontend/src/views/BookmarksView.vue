<template>
  <AppLayout>
    <div class="p-8">
      <div class="flex items-center justify-between mb-6">
        <h1 class="text-xl font-medium text-gray-900">Bookmarks</h1>
        <button
          @click="openModal()"
          class="px-4 py-2 text-sm font-medium text-white bg-purple-600 rounded-lg hover:bg-purple-700 transition-colors"
        >
          Add bookmark
        </button>
      </div>

      <div class="mb-4">
        <input
          v-model="search"
          type="text"
          placeholder="Search bookmarks..."
          class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg outline-none focus:border-purple-400 transition-colors"
        />
      </div>

      <div v-if="filteredBookmarks.length === 0" class="text-sm text-gray-400 mt-8 text-center">
        No bookmarks yet. Add your first one.
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div
          v-for="bookmark in filteredBookmarks"
          :key="bookmark.id"
          class="bg-white border border-gray-100 rounded-xl p-5 flex gap-4"
        >
          <div class="w-10 h-10 rounded-lg bg-gray-50 flex items-center justify-center shrink-0">
            <svg
              class="w-4 h-4 text-gray-400"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" />
              <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" />
            </svg>
          </div>

          <div class="flex-1 min-w-0">
            <div class="flex items-start justify-between gap-2">
              <a
                :href="bookmark.url"
                target="_blank"
                class="text-sm font-medium text-gray-900 hover:text-purple-600 transition-colors truncate"
              >
                {{ bookmark.title || bookmark.url }}
              </a>
              <button
                @click="deleteBookmark(bookmark)"
                class="text-gray-300 hover:text-red-400 transition-colors shrink-0"
              >
                <svg
                  class="w-3.5 h-3.5"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path d="M18 6L6 18M6 6l12 12" />
                </svg>
              </button>
            </div>
            <p class="text-xs text-gray-400 truncate mt-0.5">{{ bookmark.url }}</p>
            <p v-if="bookmark.description" class="text-xs text-gray-500 mt-1.5 line-clamp-2">
              {{ bookmark.description }}
            </p>
            <div class="flex gap-1 mt-2 flex-wrap">
              <span
                v-for="tag in parseTags(bookmark.tags)"
                :key="tag"
                class="text-xs bg-purple-50 text-purple-600 px-2 py-0.5 rounded"
              >
                {{ tag }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="showModal"
      class="fixed inset-0 bg-black/30 flex items-center justify-center z-50"
      @click.self="closeModal"
    >
      <div class="bg-white rounded-xl w-full max-w-md p-6">
        <h2 class="text-base font-medium text-gray-900 mb-4">Add bookmark</h2>

        <div class="mb-3">
          <input
            v-model="form.url"
            type="url"
            placeholder="https://example.com"
            class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg outline-none focus:border-purple-400 transition-colors"
          />
        </div>

        <div class="mb-5">
          <input
            v-model="form.tags"
            type="text"
            placeholder="Tags, separated by commas"
            class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg outline-none focus:border-purple-400 transition-colors"
          />
        </div>

        <p class="text-xs text-gray-400 mb-5">
          Title and description will be fetched automatically.
        </p>

        <div class="flex gap-3 justify-end">
          <button
            @click="closeModal"
            class="px-4 py-2 text-sm text-gray-500 hover:text-gray-700 transition-colors"
          >
            Cancel
          </button>
          <button
            @click="saveBookmark"
            :disabled="!form.url"
            class="px-4 py-2 text-sm font-medium text-white bg-purple-600 rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50"
          >
            Save
          </button>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import AppLayout from "@/components/layout/AppLayout.vue";
import api from "@/api/axios";
import type { Bookmark } from "@/types";

const bookmarks = ref<Bookmark[]>([]);
const search = ref("");
const showModal = ref(false);
const form = ref({ url: "", tags: "" });

const filteredBookmarks = computed(() =>
  bookmarks.value.filter(
    (b) =>
      b.title.toLowerCase().includes(search.value.toLowerCase()) ||
      b.url.toLowerCase().includes(search.value.toLowerCase()),
  ),
);

function parseTags(tags: string) {
  return tags
    ? tags
        .split(",")
        .map((t) => t.trim())
        .filter(Boolean)
    : [];
}

function openModal() {
  form.value = { url: "", tags: "" };
  showModal.value = true;
}

function closeModal() {
  showModal.value = false;
}

async function saveBookmark() {
  const { data } = await api.post("/bookmarks/", form.value);
  bookmarks.value.unshift(data);
  closeModal();
}

async function deleteBookmark(bookmark: Bookmark) {
  await api.delete(`/bookmarks/${bookmark.id}/`);
  bookmarks.value = bookmarks.value.filter((b) => b.id !== bookmark.id);
}

onMounted(async () => {
  const { data } = await api.get("/bookmarks/");
  bookmarks.value = data.results ?? data;
});
</script>
