<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { adminApi } from '@/api'
import type { DashboardStats } from '@/types'

const { t } = useI18n()
const stats = ref<DashboardStats | null>(null)

onMounted(async () => {
  try {
    const { data } = await adminApi.getStats()
    stats.value = data
  } catch {
    stats.value = null
  }
})
</script>

<template>
  <div>
    <h2 class="font-display font-semibold text-2xl mb-8 tracking-wide">{{ t('admin.dashboard') }}</h2>

    <div v-if="stats" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
      <div class="washi-panel p-6">
        <p class="text-ink-muted text-sm mb-2 tracking-wide">{{ t('admin.stats_projects') }}</p>
        <p class="text-3xl font-display font-semibold text-accent">{{ stats.projects_total }}</p>
        <p class="text-xs text-ink-faint mt-1">{{ stats.projects_published }} {{ t('admin.published') }}</p>
      </div>
      <div class="washi-panel p-6">
        <p class="text-ink-muted text-sm mb-2 tracking-wide">{{ t('admin.stats_knowledge') }}</p>
        <p class="text-3xl font-display font-semibold text-accent">{{ stats.knowledge_total }}</p>
        <p class="text-xs text-ink-faint mt-1">{{ stats.knowledge_published }} {{ t('admin.published') }}</p>
      </div>
    </div>
  </div>
</template>
