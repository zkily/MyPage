<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const skills = [
  'Vue 3', 'TypeScript', 'Python', 'FastAPI', 'MySQL',
  'Tailwind CSS', 'Docker', 'Git', 'REST API', 'UI/UX',
  'React', 'Node.js', 'Figma', 'Linux', 'Nginx',
]
</script>

<template>
  <section class="py-14 overflow-hidden border-y border-line">
    <p class="text-center text-xs text-ink-faint mb-8 tracking-[0.3em]">{{ t('skills.title') }}</p>
    <div class="relative">
      <div class="flex marquee-track whitespace-nowrap">
        <div v-for="repeat in 2" :key="repeat" class="flex shrink-0">
          <span
            v-for="skill in skills"
            :key="`${repeat}-${skill}`"
            class="mx-3 px-5 py-1.5 border border-line text-ink-muted text-sm tracking-wide hover:border-accent hover:text-accent transition-colors"
          >
            {{ skill }}
          </span>
        </div>
      </div>
    </div>
  </section>
</template>
