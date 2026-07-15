<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import MarkdownIt from 'markdown-it'
import { publicApi } from '@/api'
import { useLocaleStore } from '@/stores'
import type { Project } from '@/types'
import ProjectCard from './ProjectCard.vue'

const { t } = useI18n()
const localeStore = useLocaleStore()
const projects = ref<Project[]>([])
const loading = ref(true)
const selected = ref<Project | null>(null)
const sectionRef = ref<HTMLElement | null>(null)
const visible = ref(false)

const md = new MarkdownIt()

async function fetchProjects() {
  loading.value = true
  try {
    const { data } = await publicApi.getProjects(localeStore.currentLang)
    projects.value = data
  } catch {
    projects.value = []
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await fetchProjects()

  const observer = new IntersectionObserver(
    ([entry]) => {
      if (entry.isIntersecting) visible.value = true
    },
    { threshold: 0.1 },
  )
  if (sectionRef.value) observer.observe(sectionRef.value)
})

watch(() => localeStore.currentLang, fetchProjects)

function openProject(project: Project) {
  selected.value = project
}

function closeModal() {
  selected.value = null
}
</script>

<template>
  <section id="projects" ref="sectionRef" class="py-24 px-6 shan-shui-wash">
    <div class="max-w-6xl mx-auto">
      <div class="reveal-up mb-16 section-rule" :class="{ visible }">
        <h2 class="font-display font-semibold text-3xl md:text-4xl text-ink tracking-wide mb-3">
          {{ t('projects.title') }}
        </h2>
        <p class="text-ink-muted text-base">{{ t('projects.subtitle') }}</p>
      </div>

      <div v-if="loading" class="text-center text-ink-faint py-20 tracking-wide">Loading...</div>

      <div v-else-if="projects.length === 0" class="text-center text-ink-faint py-20 tracking-wide">
        {{ t('projects.empty') }}
      </div>

      <div
        v-else
        class="grid grid-cols-1 md:grid-cols-3 gap-5 auto-rows-auto reveal-up"
        :class="{ visible }"
      >
        <ProjectCard
          v-for="project in projects"
          :key="project.id"
          :project="project"
          @click="openProject"
        />
      </div>
    </div>

    <Teleport to="body">
      <Transition name="modal">
        <div
          v-if="selected"
          class="fixed inset-0 z-[100] flex items-center justify-center p-6 bg-ink/40 backdrop-blur-sm"
          @click.self="closeModal"
        >
          <div class="washi-panel max-w-2xl w-full max-h-[85vh] overflow-y-auto p-8">
            <img
              v-if="selected.cover_url"
              :src="selected.cover_url"
              :alt="selected.title"
              class="w-full h-48 object-cover mb-6"
            />
            <h3 class="font-display font-semibold text-2xl mb-4 text-ink tracking-wide">{{ selected.title }}</h3>
            <div class="prose prose-stone prose-sm max-w-none mb-6 text-ink-muted" v-html="md.render(selected.description)" />
            <div class="flex flex-wrap gap-2 mb-6">
              <span
                v-for="tech in selected.tech_stack"
                :key="tech"
                class="text-xs px-3 py-1 border border-line text-ink-muted tracking-wide"
              >
                {{ tech }}
              </span>
            </div>
            <div class="flex gap-3 flex-wrap">
              <a
                v-if="selected.demo_url"
                :href="selected.demo_url"
                target="_blank"
                class="btn-primary text-sm"
              >
                {{ t('projects.demo') }}
              </a>
              <a
                v-if="selected.repo_url"
                :href="selected.repo_url"
                target="_blank"
                class="btn-ghost text-sm"
              >
                {{ t('projects.source') }}
              </a>
              <button class="ml-auto btn-ghost text-sm" @click="closeModal">
                {{ t('knowledge.close') }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </section>
</template>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>
