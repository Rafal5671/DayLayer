<template>
  <AppLayout>
    <div class="p-8">
      <div class="flex items-center justify-between mb-6">
        <h1 class="text-xl font-medium text-gray-900">Tasks</h1>
        <button
          @click="openModal()"
          class="px-4 py-2 text-sm font-medium text-white bg-purple-600 rounded-lg hover:bg-purple-700 transition-colors"
        >
          New task
        </button>
      </div>

      <div class="flex gap-2 mb-6">
        <button
          v-for="f in filters"
          :key="f.value"
          @click="activeFilter = f.value"
          class="px-3 py-1.5 text-xs rounded-lg transition-colors"
          :class="
            activeFilter === f.value
              ? 'bg-purple-600 text-white'
              : 'bg-gray-100 text-gray-500 hover:bg-gray-200'
          "
        >
          {{ f.label }}
        </button>
      </div>

      <div v-if="filteredTasks.length === 0" class="text-sm text-gray-400 mt-8 text-center">
        No tasks here.
      </div>

      <div class="space-y-2">
        <div
          v-for="task in filteredTasks"
          :key="task.id"
          class="bg-white border border-gray-100 rounded-xl px-5 py-4 flex items-center gap-4"
          :class="{ 'opacity-50': task.status === 'done' }"
        >
          <div class="flex-1 min-w-0">
            <p
              class="text-sm text-gray-800"
              :class="{ 'line-through text-gray-400': task.status === 'done' }"
            >
              {{ task.title }}
            </p>
            <div class="flex items-center gap-3 mt-1">
              <p v-if="task.deadline" class="text-xs text-gray-400">
                Due {{ formatDate(task.deadline) }}
              </p>
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

          <div class="flex items-center gap-2 shrink-0">
            <button
              v-for="s in statuses"
              :key="s.value"
              @click="setStatus(task, s.value)"
              class="text-xs px-3 py-1.5 rounded-lg transition-colors border"
              :class="
                task.status === s.value
                  ? s.activeClass
                  : 'border-gray-100 text-gray-400 hover:border-gray-200 hover:text-gray-600'
              "
            >
              {{ s.label }}
            </button>
          </div>

          <button
            @click="openModal(task)"
            class="text-gray-300 hover:text-gray-500 transition-colors shrink-0"
          >
            <svg
              class="w-4 h-4"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <div
      v-if="showModal"
      class="fixed inset-0 bg-black/30 flex items-center justify-center z-50"
      @click.self="closeModal"
    >
      <div class="bg-white rounded-xl w-full max-w-md p-6">
        <h2 class="text-base font-medium text-gray-900 mb-4">
          {{ editingTask ? "Edit task" : "New task" }}
        </h2>

        <div class="mb-3">
          <input
            v-model="form.title"
            type="text"
            placeholder="Task title"
            class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg outline-none focus:border-purple-400 transition-colors"
          />
        </div>

        <div class="mb-3">
          <textarea
            v-model="form.description"
            placeholder="Description (optional)"
            rows="3"
            class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg outline-none focus:border-purple-400 transition-colors resize-none"
          />
        </div>

        <div class="grid grid-cols-2 gap-3 mb-3">
          <div>
            <label class="block text-xs text-gray-400 mb-1.5">Priority</label>
            <select
              v-model="form.priority"
              class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg outline-none focus:border-purple-400 transition-colors"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>
          <div>
            <label class="block text-xs text-gray-400 mb-1.5">Deadline</label>
            <input
              v-model="form.deadline"
              type="date"
              class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg outline-none focus:border-purple-400 transition-colors"
            />
          </div>
        </div>

        <div class="flex items-center justify-between mt-5">
          <button
            v-if="editingTask"
            @click="deleteTask"
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
              @click="saveTask"
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
import type { Task } from "@/types";

const tasks = ref<Task[]>([]);
const showModal = ref(false);
const editingTask = ref<Task | null>(null);
const activeFilter = ref("all");

const filters = [
  { label: "All", value: "all" },
  { label: "To do", value: "todo" },
  { label: "In progress", value: "in_progress" },
  { label: "Done", value: "done" },
];

const statuses = [
  { value: "todo", label: "To do", activeClass: "border-gray-400 text-gray-700 bg-gray-50" },
  {
    value: "in_progress",
    label: "In progress",
    activeClass: "border-amber-400 text-amber-700 bg-amber-50",
  },
  { value: "done", label: "Done", activeClass: "border-purple-400 text-purple-700 bg-purple-50" },
];

const form = ref({
  title: "",
  description: "",
  priority: "medium",
  deadline: "",
});

const filteredTasks = computed(() =>
  activeFilter.value === "all"
    ? tasks.value
    : tasks.value.filter((t) => t.status === activeFilter.value),
);

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString("en-GB", {
    day: "numeric",
    month: "short",
  });
}

function openModal(task?: Task) {
  if (task) {
    editingTask.value = task;
    form.value = {
      title: task.title,
      description: task.description,
      priority: task.priority,
      deadline: task.deadline ?? "",
    };
  } else {
    editingTask.value = null;
    form.value = { title: "", description: "", priority: "medium", deadline: "" };
  }
  showModal.value = true;
}

function closeModal() {
  showModal.value = false;
  editingTask.value = null;
}

async function setStatus(task: Task, status: string) {
  const { data } = await api.patch(`/tasks/${task.id}/`, { status });
  const index = tasks.value.findIndex((t) => t.id === task.id);
  tasks.value[index] = data;
}

async function saveTask() {
  const payload = {
    ...form.value,
    deadline: form.value.deadline || null,
  };
  if (editingTask.value) {
    const { data } = await api.put(`/tasks/${editingTask.value.id}/`, payload);
    const index = tasks.value.findIndex((t) => t.id === editingTask.value!.id);
    tasks.value[index] = data;
  } else {
    const { data } = await api.post("/tasks/", payload);
    tasks.value.unshift(data);
  }
  closeModal();
}

async function deleteTask() {
  if (!editingTask.value) return;
  await api.delete(`/tasks/${editingTask.value.id}/`);
  tasks.value = tasks.value.filter((t) => t.id !== editingTask.value!.id);
  closeModal();
}

onMounted(async () => {
  const { data } = await api.get("/tasks/");
  tasks.value = data.results ?? data;
});
</script>
