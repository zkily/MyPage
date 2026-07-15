<script setup lang="ts">
import { useLocaleStore } from '@/stores'
import type { LangCode } from '@/types'

const localeStore = useLocaleStore()

const langs: { code: LangCode; label: string }[] = [
  { code: 'ja', label: '日' },
  { code: 'zh', label: '中' },
  { code: 'en', label: 'EN' },
]
</script>

<template>
  <div class="flex items-center gap-0 border border-line bg-surface/70">
    <button
      v-for="lang in langs"
      :key="lang.code"
      class="px-3 py-1.5 text-xs tracking-wide transition-all duration-300"
      :class="
        localeStore.currentLang === lang.code
          ? 'bg-accent text-[#f5f3ee]'
          : 'text-ink-muted hover:text-ink'
      "
      @click="localeStore.setLang(lang.code)"
    >
      {{ lang.label }}
    </button>
  </div>
</template>
