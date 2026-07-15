<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { adminApi } from '@/api'
import type { ProjectSize } from '@/types'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()

const isNew = computed(() => route.name === 'admin-project-new')
const activeLang = ref<'ja' | 'zh' | 'en'>('ja')
const saving = ref(false)
const uploading = ref(false)

const form = ref({
  slug: '',
  title_ja: '',
  title_zh: '',
  title_en: '',
  desc_ja: '',
  desc_zh: '',
  desc_en: '',
  cover_url: '',
  tech_stack: '',
  demo_url: '',
  repo_url: '',
  size: 'medium' as ProjectSize,
  sort_order: 0,
  is_published: false,
})

const sizes: ProjectSize[] = ['small', 'medium', 'large', 'featured']

onMounted(async () => {
  if (!isNew.value) {
    const id = Number(route.params.id)
    const { data } = await adminApi.getProject(id)
    form.value = {
      slug: data.slug,
      title_ja: data.title_ja,
      title_zh: data.title_zh,
      title_en: data.title_en,
      desc_ja: data.desc_ja,
      desc_zh: data.desc_zh,
      desc_en: data.desc_en,
      cover_url: data.cover_url,
      tech_stack: (data.tech_stack || []).join(', '),
      demo_url: data.demo_url || '',
      repo_url: data.repo_url || '',
      size: data.size,
      sort_order: data.sort_order,
      is_published: data.is_published,
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
  const payload = {
    ...form.value,
    tech_stack: form.value.tech_stack.split(',').map((s) => s.trim()).filter(Boolean),
    demo_url: form.value.demo_url || null,
    repo_url: form.value.repo_url || null,
  }
  try {
    if (isNew.value) {
      await adminApi.createProject(payload)
    } else {
      await adminApi.updateProject(Number(route.params.id), payload)
    }
    router.push('/admin/projects')
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div>
    <h2 class="font-display font-semibold text-2xl mb-8 tracking-wide">
      {{ isNew ? t('admin.create') : t('admin.edit') }} — {{ t('admin.projects') }}
    </h2>

    <form class="max-w-2xl space-y-6" @submit.prevent="handleSave">
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

      <div v-show="activeLang === 'ja'">
        <label class="block text-sm text-ink-muted mb-2">{{ t('admin.title') }}</label>
        <input v-model="form.title_ja" required class="w-full px-4 py-3 bg-surface border border-line focus:border-accent outline-none transition-colors mb-4" />
        <label class="block text-sm text-ink-muted mb-2">{{ t('admin.description') }}</label>
        <textarea v-model="form.desc_ja" rows="4" class="w-full px-4 py-3 bg-surface border border-line focus:border-accent outline-none transition-colors" />
      </div>
      <div v-show="activeLang === 'zh'">
        <label class="block text-sm text-ink-muted mb-2">{{ t('admin.title') }}</label>
        <input v-model="form.title_zh" class="w-full px-4 py-3 bg-surface border border-line focus:border-accent outline-none transition-colors mb-4" />
        <label class="block text-sm text-ink-muted mb-2">{{ t('admin.description') }}</label>
        <textarea v-model="form.desc_zh" rows="4" class="w-full px-4 py-3 bg-surface border border-line focus:border-accent outline-none transition-colors" />
      </div>
      <div v-show="activeLang === 'en'">
        <label class="block text-sm text-ink-muted mb-2">{{ t('admin.title') }}</label>
        <input v-model="form.title_en" class="w-full px-4 py-3 bg-surface border border-line focus:border-accent outline-none transition-colors mb-4" />
        <label class="block text-sm text-ink-muted mb-2">{{ t('admin.description') }}</label>
        <textarea v-model="form.desc_en" rows="4" class="w-full px-4 py-3 bg-surface border border-line focus:border-accent outline-none transition-colors" />
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
        <label class="block text-sm text-ink-muted mb-2">{{ t('admin.tech_stack') }}</label>
        <input v-model="form.tech_stack" class="w-full px-4 py-3 bg-surface border border-line focus:border-accent outline-none transition-colors" placeholder="Vue, Python, MySQL" />
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm text-ink-muted mb-2">{{ t('admin.demo_url') }}</label>
          <input v-model="form.demo_url" class="w-full px-4 py-3 bg-surface border border-line focus:border-accent outline-none transition-colors" />
        </div>
        <div>
          <label class="block text-sm text-ink-muted mb-2">{{ t('admin.repo_url') }}</label>
          <input v-model="form.repo_url" class="w-full px-4 py-3 bg-surface border border-line focus:border-accent outline-none transition-colors" />
        </div>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm text-ink-muted mb-2">{{ t('admin.size') }}</label>
          <select v-model="form.size" class="w-full px-4 py-3 bg-surface border border-line focus:border-accent outline-none transition-colors">
            <option v-for="s in sizes" :key="s" :value="s">{{ s }}</option>
          </select>
        </div>
        <div>
          <label class="block text-sm text-ink-muted mb-2">{{ t('admin.sort_order') }}</label>
          <input v-model.number="form.sort_order" type="number" class="w-full px-4 py-3 bg-surface border border-line focus:border-accent outline-none transition-colors" />
        </div>
      </div>

      <label class="flex items-center gap-3 cursor-pointer">
        <input v-model="form.is_published" type="checkbox" class="w-4 h-4 accent-accent" />
        <span class="text-sm">{{ t('admin.published') }}</span>
      </label>

      <div class="flex gap-3 pt-4">
        <button type="submit" :disabled="saving" class="btn-primary text-sm disabled:opacity-50">
          {{ t('admin.save') }}
        </button>
        <button type="button" class="btn-ghost text-sm" @click="router.push('/admin/projects')">
          {{ t('admin.cancel') }}
        </button>
      </div>
    </form>
  </div>
</template>
