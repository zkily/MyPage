<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import type { Project, ProjectSize } from '@/types'

const props = defineProps<{
  project: Project
}>()

defineEmits<{
  click: [project: Project]
}>()

const { t } = useI18n()

const sizeClass = computed(() => {
  const map: Record<ProjectSize, string> = {
    featured: 'md:col-span-2 md:row-span-2',
    large: 'md:col-span-2',
    medium: 'md:col-span-1',
    small: 'md:col-span-1',
  }
  return map[props.project.size]
})

const imageHeight = computed(() => {
  const map: Record<ProjectSize, string> = {
    featured: 'h-64 md:h-80',
    large: 'h-48 md:h-56',
    medium: 'h-44',
    small: 'h-40',
  }
  return map[props.project.size]
})
</script>

<template>
  <article
    class="washi-panel group cursor-pointer overflow-hidden transition-all duration-500 hover:-translate-y-1"
    :class="sizeClass"
    @click="$emit('click', project)"
  >
    <div class="relative overflow-hidden" :class="imageHeight">
      <img
        v-if="project.cover_url"
        :src="project.cover_url"
        :alt="project.title"
        class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
      />
      <div v-else class="w-full h-full bg-surface-hover flex items-center justify-center text-ink-faint font-display tracking-wide">
        No Image
      </div>
      <div class="absolute inset-0 bg-gradient-to-t from-bg/80 via-transparent to-transparent" />
    </div>

    <div class="p-5 relative">
      <h3 class="font-display font-semibold text-lg mb-2 text-ink group-hover:text-accent transition-colors tracking-wide">
        {{ project.title }}
      </h3>
      <p class="text-ink-muted text-sm line-clamp-2 mb-4 leading-relaxed">{{ project.description }}</p>

      <div class="flex flex-wrap gap-2 mb-4">
        <span
          v-for="tech in project.tech_stack.slice(0, 4)"
          :key="tech"
          class="text-xs px-2 py-1 border border-line text-ink-faint tracking-wide"
        >
          {{ tech }}
        </span>
      </div>

      <div class="flex gap-4">
        <a
          v-if="project.demo_url"
          :href="project.demo_url"
          target="_blank"
          rel="noopener"
          class="text-xs text-accent hover:underline tracking-wide"
          @click.stop
        >
          {{ t('projects.demo') }} →
        </a>
        <a
          v-if="project.repo_url"
          :href="project.repo_url"
          target="_blank"
          rel="noopener"
          class="text-xs text-wood hover:underline tracking-wide"
          @click.stop
        >
          {{ t('projects.source') }} →
        </a>
      </div>
    </div>
  </article>
</template>
