<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import MarkdownIt from 'markdown-it'
import { publicApi } from '@/api'
import { useLocaleStore } from '@/stores'
import {
  projectMatchesSection,
  projectSections,
  type ProjectSection,
} from '@/config/projectMenu'
import type { Project } from '@/types'

const { t } = useI18n()
const localeStore = useLocaleStore()

const projects = ref<Project[]>([])
const loading = ref(true)
const activeSectionId = ref(projectSections[0]?.id ?? 'all')
const selectedId = ref<number | null>(null)
const mobileMenuOpen = ref(false)

const md = new MarkdownIt()

const activeSection = computed(
  () => projectSections.find((s) => s.id === activeSectionId.value) ?? projectSections[0],
)

const filteredProjects = computed(() => {
  const section = activeSection.value
  if (!section) return projects.value
  return projects.value.filter((p) => projectMatchesSection(p, section))
})

const selected = computed(
  () => projects.value.find((p) => p.id === selectedId.value) ?? null,
)

async function fetchProjects() {
  loading.value = true
  try {
    const { data } = await publicApi.getProjects(localeStore.currentLang)
    projects.value = data
    if (selectedId.value && !data.some((p: Project) => p.id === selectedId.value)) {
      selectedId.value = null
    }
  } catch {
    projects.value = []
  } finally {
    loading.value = false
  }
}

function selectSection(section: ProjectSection) {
  activeSectionId.value = section.id
  selectedId.value = null
  mobileMenuOpen.value = false
}

function openProject(project: Project) {
  selectedId.value = project.id
  mobileMenuOpen.value = false
}

onMounted(fetchProjects)
watch(() => localeStore.currentLang, fetchProjects)
</script>

<template>
  <section class="pt-28 pb-16 px-4 sm:px-6 min-h-[calc(100vh-4rem)]">
    <div class="max-w-6xl mx-auto mb-8 md:mb-10">
      <h1 class="font-display font-semibold text-3xl md:text-4xl text-ink tracking-wide mb-3 section-rule">
        {{ t('projects.title') }}
      </h1>
      <p class="text-ink-muted text-base mt-6">{{ t('projects.subtitle') }}</p>
    </div>

    <div class="md:hidden max-w-6xl mx-auto mb-4">
      <button
        type="button"
        class="btn-ghost text-sm w-full justify-between"
        @click="mobileMenuOpen = !mobileMenuOpen"
      >
        <span>{{ t(`projects.sections.${activeSectionId}`) }}</span>
        <span class="text-ink-faint">{{ mobileMenuOpen ? '▲' : '▼' }}</span>
      </button>
    </div>

    <div class="max-w-6xl mx-auto flex flex-col md:flex-row gap-0 md:gap-10 md:items-start border border-line bg-surface/40">
      <aside
        class="md:w-64 shrink-0 border-b md:border-b-0 md:border-r border-line"
        :class="mobileMenuOpen ? 'block' : 'hidden md:block'"
      >
        <div class="p-5 md:p-6 md:sticky md:top-24 md:max-h-[calc(100vh-7rem)] md:overflow-y-auto">
          <p class="text-xs text-ink-faint tracking-[0.25em] mb-4">
            {{ t('projects.menu_title') }}
          </p>

          <nav class="space-y-1 mb-8">
            <button
              v-for="section in projectSections"
              :key="section.id"
              type="button"
              class="w-full text-left px-3 py-2.5 text-sm tracking-wide transition-colors border-l-2"
              :class="
                activeSectionId === section.id
                  ? 'border-accent text-ink bg-surface-hover/60'
                  : 'border-transparent text-ink-muted hover:text-ink hover:bg-surface-hover/40'
              "
              @click="selectSection(section)"
            >
              {{ t(`projects.sections.${section.id}`) }}
            </button>
          </nav>

          <p class="text-xs text-ink-faint tracking-[0.25em] mb-3">
            {{ t('projects.item_list') }}
          </p>

          <div v-if="loading" class="text-xs text-ink-faint py-4">Loading...</div>
          <ul v-else-if="filteredProjects.length" class="space-y-1">
            <li v-for="project in filteredProjects" :key="project.id">
              <button
                type="button"
                class="w-full text-left px-3 py-2 text-sm tracking-wide transition-colors"
                :class="selectedId === project.id ? 'text-accent' : 'text-ink-muted hover:text-ink'"
                @click="openProject(project)"
              >
                <span class="line-clamp-2">{{ project.title }}</span>
              </button>
            </li>
          </ul>
          <p v-else class="text-xs text-ink-faint px-3 py-2 leading-relaxed">
            {{ t('projects.section_empty') }}
          </p>
        </div>
      </aside>

      <div class="flex-1 min-w-0 p-6 md:p-10 min-h-[28rem]">
        <template v-if="!selected">
          <h2 class="font-display text-2xl text-ink tracking-wide mb-2">
            {{ t(`projects.sections.${activeSectionId}`) }}
          </h2>
          <p class="text-ink-muted text-sm mb-10 leading-relaxed">
            {{ t(`projects.section_desc.${activeSectionId}`) }}
          </p>

          <div v-if="loading" class="text-ink-faint tracking-wide py-12">Loading...</div>
          <div v-else-if="filteredProjects.length === 0" class="text-ink-faint tracking-wide py-12">
            {{ t('projects.section_empty') }}
          </div>

          <ul v-else class="space-y-0 divide-y divide-line border-t border-line">
            <li v-for="project in filteredProjects" :key="project.id">
              <button
                type="button"
                class="w-full text-left py-6 group hover:bg-surface-hover/30 transition-colors -mx-2 px-2"
                @click="openProject(project)"
              >
                <div class="flex gap-4">
                  <div
                    v-if="project.cover_url"
                    class="hidden sm:block w-28 h-20 shrink-0 border border-line overflow-hidden bg-surface"
                  >
                    <img
                      :src="project.cover_url"
                      :alt="project.title"
                      class="w-full h-full object-cover"
                      loading="lazy"
                    />
                  </div>
                  <div class="min-w-0">
                    <h3 class="font-display text-lg text-ink group-hover:text-accent transition-colors tracking-wide mb-2">
                      {{ project.title }}
                    </h3>
                    <p class="text-sm text-ink-muted line-clamp-2 leading-relaxed mb-3">
                      {{ project.description }}
                    </p>
                    <div class="flex flex-wrap gap-2">
                      <span
                        v-for="tech in project.tech_stack.slice(0, 4)"
                        :key="tech"
                        class="text-xs text-ink-faint tracking-wide"
                      >
                        {{ tech }}
                      </span>
                    </div>
                  </div>
                </div>
              </button>
            </li>
          </ul>
        </template>

        <template v-else>
          <button
            type="button"
            class="text-sm text-ink-faint hover:text-ink tracking-wide mb-8 transition-colors"
            @click="selectedId = null"
          >
            ← {{ t('projects.back_list') }}
          </button>

          <article>
            <img
              v-if="selected.cover_url"
              :src="selected.cover_url"
              :alt="selected.title"
              class="w-full max-h-64 object-cover border border-line mb-8"
            />
            <h2 class="font-display font-semibold text-2xl md:text-3xl text-ink tracking-wide mb-4">
              {{ selected.title }}
            </h2>
            <div
              class="prose prose-stone prose-sm md:prose-base max-w-none text-ink-muted mb-8"
              v-html="md.render(selected.description)"
            />
            <div class="flex flex-wrap gap-2 mb-8">
              <span
                v-for="tech in selected.tech_stack"
                :key="tech"
                class="text-xs px-2.5 py-1 border border-line text-ink-muted tracking-wide"
              >
                {{ tech }}
              </span>
            </div>
            <div class="flex flex-wrap gap-3">
              <a
                v-if="selected.demo_url"
                :href="selected.demo_url"
                target="_blank"
                rel="noopener"
                class="btn-primary text-sm"
              >
                {{ t('projects.demo') }}
              </a>
              <a
                v-if="selected.repo_url"
                :href="selected.repo_url"
                target="_blank"
                rel="noopener"
                class="btn-ghost text-sm"
              >
                {{ t('projects.source') }}
              </a>
            </div>
          </article>
        </template>
      </div>
    </div>
  </section>
</template>
