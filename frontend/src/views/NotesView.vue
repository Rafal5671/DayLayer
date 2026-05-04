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

      <div class="mb-6">
        <input
          v-model="search"
          type="text"
          placeholder="Search notes..."
          class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg outline-none focus:border-purple-400 transition-colors"
        />
      </div>

      <div v-if="filteredNotes.length === 0" class="text-sm text-gray-400 mt-8 text-center">
        No notes yet. Create your first one.
      </div>

      <div class="grid grid-cols-3 gap-4">
        <div
          v-for="note in filteredNotes"
          :key="note.id"
          class="bg-white border border-gray-100 rounded-xl p-5 cursor-pointer hover:border-purple-200 hover:shadow-sm transition-all flex flex-col gap-3"
          @click="openNote(note)"
        >
          <h3 class="text-sm font-medium text-gray-900 truncate">{{ note.title }}</h3>
          <div
            class="text-xs text-gray-400 line-clamp-4 flex-1 prose prose-xs max-w-none"
            v-html="renderPreview(note.content)"
          />
          <div class="flex items-center justify-between mt-auto">
            <div class="flex gap-1 flex-wrap">
              <span
                v-for="tag in parseTags(note.tags)"
                :key="tag"
                class="text-xs bg-purple-50 text-purple-600 px-2 py-0.5 rounded"
              >
                {{ tag }}
              </span>
            </div>
            <span class="text-xs text-gray-300">{{ formatDate(note.updated_at) }}</span>
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="showModal"
      class="fixed inset-0 bg-black/40 flex items-center justify-center z-50"
      @click.self="closeModal"
    >
      <div class="bg-white rounded-xl w-full max-w-4xl mx-4 flex flex-col" style="height: 85vh">
        <div class="flex items-center justify-between px-6 py-4 border-b border-gray-100">
          <input
            v-model="form.title"
            type="text"
            placeholder="Note title"
            class="text-lg font-medium text-gray-900 outline-none flex-1 placeholder:text-gray-300"
          />
          <div class="flex items-center gap-3 ml-4">
            <button
              @click="activeTab = 'write'"
              class="text-xs px-3 py-1.5 rounded-lg transition-colors"
              :class="
                activeTab === 'write'
                  ? 'bg-purple-600 text-white'
                  : 'text-gray-400 hover:text-gray-600'
              "
            >
              Write
            </button>
            <button
              @click="activeTab = 'preview'"
              class="text-xs px-3 py-1.5 rounded-lg transition-colors"
              :class="
                activeTab === 'preview'
                  ? 'bg-purple-600 text-white'
                  : 'text-gray-400 hover:text-gray-600'
              "
            >
              Preview
            </button>
            <button
              @click="closeModal"
              class="text-gray-300 hover:text-gray-500 transition-colors ml-2"
            >
              <svg
                class="w-5 h-5"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <path d="M18 6L6 18M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <div class="flex-1 overflow-hidden">
          <textarea
            v-if="activeTab === 'write'"
            v-model="form.content"
            placeholder="Write your note in Markdown...

# Heading
**bold**, *italic*
- list item
```code```"
            class="w-full h-full px-6 py-4 text-sm text-gray-700 outline-none resize-none font-mono leading-relaxed"
          />
          <div
            v-else
            class="w-full h-full px-6 py-4 overflow-y-auto prose prose-sm max-w-none"
            v-html="renderedContent"
          />
        </div>

        <div class="px-6 py-4 border-t border-gray-100 flex items-center justify-between">
          <div class="flex items-center gap-3 flex-1">
            <svg
              class="w-4 h-4 text-gray-300 shrink-0"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"
              />
              <line x1="7" y1="7" x2="7.01" y2="7" />
            </svg>
            <input
              v-model="form.tags"
              type="text"
              placeholder="tags, separated by commas"
              class="text-sm text-gray-500 outline-none flex-1 placeholder:text-gray-300"
            />
          </div>

          <div class="flex items-center gap-3">
            <button
              v-if="editingNote"
              @click="deleteNote"
              class="text-sm text-red-400 hover:text-red-600 transition-colors"
            >
              Delete
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
import { marked } from "marked";
import AppLayout from "@/components/layout/AppLayout.vue";
import api from "@/api/axios";
import type { Note } from "@/types";

const notes = ref<Note[]>([]);
const search = ref("");
const showModal = ref(false);
const editingNote = ref<Note | null>(null);
const activeTab = ref<"write" | "preview">("write");

const form = ref({ title: "", content: "", tags: "" });

const filteredNotes = computed(() =>
  notes.value.filter(
    (n) =>
      n.title.toLowerCase().includes(search.value.toLowerCase()) ||
      n.content.toLowerCase().includes(search.value.toLowerCase()),
  ),
);

const renderedContent = computed(() => marked(form.value.content || "") as string);

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

function openNote(note: Note) {
  editingNote.value = note;
  form.value = { title: note.title, content: note.content, tags: note.tags };
  activeTab.value = "write";
  showModal.value = true;
}

function openModal() {
  editingNote.value = null;
  form.value = { title: "", content: "", tags: "" };
  activeTab.value = "write";
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

function renderPreview(content: string) {
  return marked(content || "") as string;
}

onMounted(async () => {
  const { data } = await api.get("/notes/");
  notes.value = data.results ?? data;
});
</script>
