<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import { adminApi } from '@/api'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()

const isNew = computed(() => route.name === 'admin-knowledge-new')
const activeLang = ref<'ja' | 'zh' | 'en'>('ja')
const saving = ref(false)
const uploading = ref(false)

const form = ref({
  slug: '',
  title_ja: '',
  title_zh: '',
  title_en: '',
  summary_ja: '',
  summary_zh: '',
  summary_en: '',
  content_ja: '',
  content_zh: '',
  content_en: '',
  category: '',
  tags: '',
  cover_url: '',
  is_published: false,
  published_at: '',
})

onMounted(async () => {
  if (!isNew.value) {
    const id = Number(route.params.id)
    const { data } = await adminApi.getKnowledge(id)
    form.value = {
      slug: data.slug,
      title_ja: data.title_ja,
      title_zh: data.title_zh,
      title_en: data.title_en,
      summary_ja: data.summary_ja,
      summary_zh: data.summary_zh,
      summary_en: data.summary_en,
      content_ja: data.content_ja,
      content_zh: data.content_zh,
      content_en: data.content_en,
      category: data.category,
      tags: (data.tags || []).join(', '),
      cover_url: data.cover_url || '',
      is_published: data.is_published,
      published_at: data.published_at ? data.published_at.slice(0, 16) : '',
    }
  }
})

async function handleUpload(e: Event) {
  const input = e.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return
  uploading.value = true
  try {
    const { data } = await adminApi.upload(file)
    form.value.cover_url = data.url
  } finally {
    uploading.value = false
  }
}

async function handleSave() {
  saving.value = true
  const payload: Record<string, unknown> = {
    ...form.value,
    tags: form.value.tags.split(',').map((s) => s.trim()).filter(Boolean),
    cover_url: form.value.cover_url || null,
    published_at: form.value.published_at ? new Date(form.value.published_at).toISOString() : null,
  }
  try {
    if (isNew.value) {
      await adminApi.createKnowledge(payload)
    } else {
      await adminApi.updateKnowledge(Number(route.params.id), payload)
    }
    router.push('/admin/knowledge')
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div>
    <h2 class="font-display font-semibold text-2xl mb-8 tracking-wide">
      {{ isNew ? t('admin.create') : t('admin.edit') }} — {{ t('admin.knowledge') }}
    </h2>

    <form class="max-w-3xl space-y-6" @submit.prevent="handleSave">
      <div>
        <label class="block text-sm text-ink-muted mb-2">{{ t('admin.slug') }}</label>
        <input v-model="form.slug" required class="w-full px-4 py-3 bg-surface border border-line focus:border-accent outline-none transition-colors" />
      </div>

      <div class="flex gap-2 mb-4">
        <button
          v-for="lang in (['ja', 'zh', 'en'] as const)"
          :key="lang"
          type="button"
          class="px-4 py-1 text-sm transition-colors border border-line"
          :class="activeLang === lang ? 'bg-accent text-[#f5f3ee] border-accent' : 'text-ink-muted hover:text-ink'"
          @click="activeLang = lang"
        >
          {{ t(`admin.lang_${lang}`) }}
        </button>
      </div>

      <template v-if="activeLang === 'ja'">
        <div>
          <label class="block text-sm text-ink-muted mb-2">{{ t('admin.title') }}</label>
          <input v-model="form.title_ja" required class="w-full px-4 py-3 bg-surface border border-line focus:border-accent outline-none transition-colors" />
        </div>
        <div>
          <label class="block text-sm text-ink-muted mb-2">{{ t('admin.summary') }}</label>
          <textarea v-model="form.summary_ja" rows="2" class="w-full px-4 py-3 bg-surface border border-line focus:border-accent outline-none transition-colors" />
        </div>
        <div>
          <label class="block text-sm text-ink-muted mb-2">{{ t('admin.content') }}</label>
          <MdEditor v-model="form.content_ja" language="ja-JP" theme="light" />
        </div>
      </template>

      <template v-if="activeLang === 'zh'">
        <div>
          <label class="block text-sm text-ink-muted mb-2">{{ t('admin.title') }}</label>
          <input v-model="form.title_zh" class="w-full px-4 py-3 bg-surface border border-line focus:border-accent outline-none transition-colors" />
        </div>
        <div>
          <label class="block text-sm text-ink-muted mb-2">{{ t('admin.summary') }}</label>
          <textarea v-model="form.summary_zh" rows="2" class="w-full px-4 py-3 bg-surface border border-line focus:border-accent outline-none transition-colors" />
        </div>
        <div>
          <label class="block text-sm text-ink-muted mb-2">{{ t('admin.content') }}</label>
          <MdEditor v-model="form.content_zh" language="zh-CN" theme="light" />
        </div>
      </template>

      <template v-if="activeLang === 'en'">
        <div>
          <label class="block text-sm text-ink-muted mb-2">{{ t('admin.title') }}</label>
          <input v-model="form.title_en" class="w-full px-4 py-3 bg-surface border border-line focus:border-accent outline-none transition-colors" />
        </div>
        <div>
          <label class="block text-sm text-ink-muted mb-2">{{ t('admin.summary') }}</label>
          <textarea v-model="form.summary_en" rows="2" class="w-full px-4 py-3 bg-surface border border-line focus:border-accent outline-none transition-colors" />
        </div>
        <div>
          <label class="block text-sm text-ink-muted mb-2">{{ t('admin.content') }}</label>
          <MdEditor v-model="form.content_en" language="en-US" theme="light" />
        </div>
      </template>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm text-ink-muted mb-2">{{ t('admin.category') }}</label>
          <input v-model="form.category" class="w-full px-4 py-3 bg-surface border border-line focus:border-accent outline-none transition-colors" />
        </div>
        <div>
          <label class="block text-sm text-ink-muted mb-2">{{ t('admin.tags') }}</label>
          <input v-model="form.tags" class="w-full px-4 py-3 bg-surface border border-line focus:border-accent outline-none transition-colors" />
        </div>
      </div>

      <div>
        <label class="block text-sm text-ink-muted mb-2">{{ t('admin.cover') }}</label>
        <div class="flex gap-3">
          <input v-model="form.cover_url" class="w-full px-4 py-3 bg-surface border border-line focus:border-accent outline-none transition-colors flex-1" />
          <label class="px-4 py-2 border border-line text-sm cursor-pointer hover:border-ink-muted shrink-0">
            {{ uploading ? '...' : t('admin.upload') }}
            <input type="file" accept="image/*" class="hidden" @change="handleUpload" />
          </label>
        </div>
      </div>

      <div>
        <label class="block text-sm text-ink-muted mb-2">Published At</label>
        <input v-model="form.published_at" type="datetime-local" class="w-full px-4 py-3 bg-surface border border-line focus:border-accent outline-none transition-colors" />
      </div>

      <label class="flex items-center gap-3 cursor-pointer">
        <input v-model="form.is_published" type="checkbox" class="w-4 h-4 accent-accent" />
        <span class="text-sm">{{ t('admin.published') }}</span>
      </label>

      <div class="flex gap-3 pt-4">
        <button type="submit" :disabled="saving" class="btn-primary text-sm disabled:opacity-50">
          {{ t('admin.save') }}
        </button>
        <button type="button" class="btn-ghost text-sm" @click="router.push('/admin/knowledge')">
          {{ t('admin.cancel') }}
        </button>
      </div>
    </form>
  </div>
</template>
