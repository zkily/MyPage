<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { RouterLink } from 'vue-router'
import { publicApi } from '@/api'
import { useLocaleStore } from '@/stores'
import type { KnowledgeListItem, Project } from '@/types'

type CoverItem = {
  key: string
  title: string
  cover: string
  to: string
  kind: 'project' | 'knowledge'
}

const { t } = useI18n()
const localeStore = useLocaleStore()
const items = ref<CoverItem[]>([])
const failed = ref<Set<string>>(new Set())

async function load() {
  try {
    const [projectsRes, knowledgeRes] = await Promise.all([
      publicApi.getProjects(localeStore.currentLang),
      publicApi.getKnowledge(localeStore.currentLang),
    ])
    const projects = (projectsRes.data as Project[])
      .filter((p) => p.cover_url)
      .map((p) => ({
        key: `p-${p.id}`,
        title: p.title,
        cover: p.cover_url,
        to: '/projects',
        kind: 'project' as const,
      }))
    const knowledge = (knowledgeRes.data as KnowledgeListItem[])
      .filter((a) => a.cover_url)
      .map((a) => ({
        key: `k-${a.id}`,
        title: a.title,
        cover: a.cover_url as string,
        to: '/knowledge',
        kind: 'knowledge' as const,
      }))
    // 交错排列：作品 / 知识
    const merged: CoverItem[] = []
    const max = Math.max(projects.length, knowledge.length)
    for (let i = 0; i < max; i++) {
      if (projects[i]) merged.push(projects[i])
      if (knowledge[i]) merged.push(knowledge[i])
    }
    items.value = merged
  } catch {
    items.value = []
  }
}

const track = computed(() => {
  if (items.value.length === 0) return []
  // 至少铺满两遍，保证无缝循环
  const base = items.value.length < 4 ? [...items.value, ...items.value] : items.value
  return [...base, ...base]
})

function onImgError(key: string) {
  failed.value = new Set(failed.value).add(key)
}

onMounted(load)
watch(() => localeStore.currentLang, load)
</script>

<template>
  <section v-if="track.length" class="py-12 overflow-hidden border-y border-line">
    <p class="text-center text-xs text-ink-faint mb-8 tracking-[0.3em]">{{ t('home.gallery') }}</p>
    <div class="relative">
      <div class="flex marquee-track gap-4 w-max pl-4">
        <RouterLink
          v-for="(item, index) in track"
          :key="`${item.key}-${index}`"
          :to="item.to"
          class="group relative shrink-0 w-52 sm:w-64 h-36 sm:h-44 overflow-hidden border border-line bg-surface"
        >
          <img
            v-if="!failed.has(item.key)"
            :src="item.cover"
            :alt="item.title"
            class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
            loading="lazy"
            @error="onImgError(item.key)"
          />
          <div
            v-else
            class="w-full h-full flex items-center justify-center font-display text-ink-faint text-sm tracking-wide px-4 text-center"
          >
            {{ item.title }}
          </div>
          <div
            class="absolute inset-0 bg-gradient-to-t from-ink/55 via-transparent to-transparent opacity-80"
          />
          <div class="absolute bottom-0 left-0 right-0 p-3">
            <span class="text-[10px] tracking-[0.2em] text-[#f5f3ee]/80">
              {{ item.kind === 'project' ? t('nav.projects') : t('nav.knowledge') }}
            </span>
            <p class="font-display text-sm text-[#f5f3ee] tracking-wide truncate mt-0.5">
              {{ item.title }}
            </p>
          </div>
        </RouterLink>
      </div>
    </div>
  </section>
</template>
