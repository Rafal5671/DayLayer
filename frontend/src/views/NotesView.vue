<template>
  <AppLayout>
    <div class="p-8">
      <div class="flex items-center justify-between mb-6">
        <h1 class="text-xl font-medium text-gray-900">Notes</h1>
        <button
          @click="openModal()"
          class="px-4 py-2 text-sm font-medium text-white bg-purple-600 rounded-lg hover:bg-purple-700 transition-colors"
        >
          New note
        </button>
      </div>

      <div class="mb-4 flex gap-3">
        <input
          v-model="search"
          type="text"
          placeholder="Search notes..."
          class="flex-1 px-3 py-2 text-sm border border-gray-200 rounded-lg outline-none focus:border-purple-400 transition-colors"
        />
      </div>

      <div v-if="filteredNotes.length === 0" class="text-sm text-gray-400 mt-8 text-center">
        No notes yet. Create your first one.
      </div>

      <div class="grid grid-cols-3 gap-4">
        <div
          v-for="note in filteredNotes"
          :key="note.id"
          class="bg-white border border-gray-100 rounded-xl p-5 cursor-pointer hover:border-purple-200 transition-colors"
          @click="openModal(note)"
        >
          <h3 class="text-sm font-medium text-gray-900 mb-2 truncate">{{ note.title }}</h3>
          <p class="text-xs text-gray-400 line-clamp-3 mb-4">{{ note.content }}</p>
          <div class="flex items-center justify-between">
            <div class="flex gap-1 flex-wrap">
              <span
                v-for="tag in parseTags(note.tags)"
                :key="tag"
                class="text-xs bg-purple-50 text-purple-600 px-2 py-0.5 rounded"
              >
                {{ tag }}
              </span>
            </div>
            <span class="text-xs text-gray-400">{{ formatDate(note.updated_at) }}</span>
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="showModal"
      class="fixed inset-0 bg-black/30 flex items-center justify-center z-50"
      @click.self="closeModal"
    >
      <div class="bg-white rounded-xl w-full max-w-lg p-6 shadow-xl">
        <h2 class="text-base font-medium text-gray-900 mb-4">
          {{ editingNote ? "Edit note" : "New note" }}
        </h2>

        <div class="mb-3">
          <input
            v-model="form.title"
            type="text"
            placeholder="Title"
            class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg outline-none focus:border-purple-400 transition-colors"
          />
        </div>

        <div class="mb-3">
          <textarea
            v-model="form.content"
            placeholder="Write your note in Markdown..."
            rows="8"
            class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg outline-none focus:border-purple-400 transition-colors resize-none font-mono"
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

        <div class="flex items-center justify-between">
          <button
            v-if="editingNote"
            @click="deleteNote"
            class="text-sm text-red-500 hover:text-red-700 transition-colors"
          >
            Delete
          </button>
          <div class="flex gap-3 ml-auto">
            <button
              @click="closeModal"
              class="px-4 py-2 text-sm text-gray-500 hover:text-gray-700 transition-colors"
            >
              Cancel
            </button>
            <button
              @click="saveNote"
              :disabled="!form.title"
              class="px-4 py-2 text-sm font-medium text-white bg-purple-600 rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50"
            >
              Save
            </button>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import AppLayout from "@/components/layout/AppLayout.vue";
import api from "@/api/axios";
import type { Note } from "@/types";

const notes = ref<Note[]>([]);
const search = ref("");
const showModal = ref(false);
const editingNote = ref<Note | null>(null);

const form = ref({ title: "", content: "", tags: "" });

const filteredNotes = computed(() =>
  notes.value.filter(
    (n) =>
      n.title.toLowerCase().includes(search.value.toLowerCase()) ||
      n.content.toLowerCase().includes(search.value.toLowerCase()),
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

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString("en-GB", {
    day: "numeric",
    month: "short",
  });
}

function openModal(note?: Note) {
  if (note) {
    editingNote.value = note;
    form.value = { title: note.title, content: note.content, tags: note.tags };
  } else {
    editingNote.value = null;
    form.value = { title: "", content: "", tags: "" };
  }
  showModal.value = true;
}

function closeModal() {
  showModal.value = false;
  editingNote.value = null;
}

async function saveNote() {
  if (editingNote.value) {
    const { data } = await api.put(`/notes/${editingNote.value.id}/`, form.value);
    const index = notes.value.findIndex((n) => n.id === editingNote.value!.id);
    notes.value[index] = data;
  } else {
    const { data } = await api.post("/notes/", form.value);
    notes.value.unshift(data);
  }
  closeModal();
}

async function deleteNote() {
  if (!editingNote.value) return;
  await api.delete(`/notes/${editingNote.value.id}/`);
  notes.value = notes.value.filter((n) => n.id !== editingNote.value!.id);
  closeModal();
}

onMounted(async () => {
  const { data } = await api.get("/notes/");
  notes.value = data.results ?? data;
});
</script>
