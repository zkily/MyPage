<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { adminApi } from '@/api'
import type { KnowledgeAdmin } from '@/types'

const { t } = useI18n()
const router = useRouter()
const articles = ref<KnowledgeAdmin[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await adminApi.listKnowledge()
    articles.value = data
  } finally {
    loading.value = false
  }
})

async function handleDelete(id: number) {
  if (!confirm(t('admin.confirm_delete'))) return
  await adminApi.deleteKnowledge(id)
  articles.value = articles.value.filter((a) => a.id !== id)
}
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-8">
      <h2 class="font-display font-semibold text-2xl tracking-wide">{{ t('admin.knowledge') }}</h2>
      <router-link to="/admin/knowledge/new" class="btn-primary text-sm">
        + {{ t('admin.create') }}
      </router-link>
    </div>

    <div v-if="loading" class="text-ink-faint tracking-wide">Loading...</div>

    <div v-else class="space-y-3">
      <div
        v-for="article in articles"
        :key="article.id"
        class="washi-panel p-4 flex items-center justify-between gap-4"
      >
        <div class="min-w-0">
          <h3 class="font-medium truncate">{{ article.title_ja }}</h3>
          <p class="text-xs text-ink-faint">{{ article.slug }} · {{ article.category }}</p>
        </div>
        <div class="flex items-center gap-3 shrink-0">
          <span
            class="text-xs px-2 py-1 border"
            :class="article.is_published ? 'border-accent-soft text-accent-soft' : 'border-line text-ink-faint'"
          >
            {{ article.is_published ? t('admin.published') : t('admin.draft') }}
          </span>
          <button
            class="text-sm text-accent hover:underline"
            @click="router.push(`/admin/knowledge/${article.id}`)"
          >
            {{ t('admin.edit') }}
          </button>
          <button class="text-sm text-red-700/70 hover:underline" @click="handleDelete(article.id)">
            {{ t('admin.delete') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
