<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import type { KnowledgeListItem } from '@/types'

defineProps<{
  article: KnowledgeListItem
  index: number
}>()

defineEmits<{
  click: [article: KnowledgeListItem]
}>()

const { t } = useI18n()

function formatDate(date: string | null) {
  if (!date) return ''
  return new Date(date).toLocaleDateString()
}
</script>

<template>
  <article
    class="relative pl-10 pb-12 group cursor-pointer reveal-up visible"
    :style="{ transitionDelay: `${index * 100}ms` }"
    @click="$emit('click', article)"
  >
    <div
      class="absolute left-0 top-2 w-2.5 h-2.5 rounded-full border border-accent bg-bg group-hover:bg-accent transition-all duration-300"
    />
    <div
      class="absolute left-[4px] top-5 w-px h-full bg-line"
    />

    <time class="text-xs text-ink-faint mb-2 block tracking-wide">{{ formatDate(article.published_at) }}</time>

    <div class="washi-panel p-6 transition-all duration-300 group-hover:-translate-y-0.5">
      <span
        v-if="article.category"
        class="inline-block text-xs px-2.5 py-1 border border-line text-accent mb-3 tracking-wide"
      >
        {{ article.category }}
      </span>

      <h3 class="font-display font-semibold text-xl mb-2 text-ink group-hover:text-accent transition-colors tracking-wide">
        {{ article.title }}
      </h3>

      <p class="text-ink-muted text-sm line-clamp-3 mb-4 leading-relaxed">{{ article.summary }}</p>

      <div class="flex flex-wrap gap-2 mb-4">
        <span
          v-for="tag in article.tags"
          :key="tag"
          class="text-xs px-2 py-0.5 text-ink-faint tracking-wide"
        >
          #{{ tag }}
        </span>
      </div>

      <span class="text-sm text-accent group-hover:underline tracking-wide">
        {{ t('knowledge.readMore') }} →
      </span>
    </div>
  </article>
</template>
