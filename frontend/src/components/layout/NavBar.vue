<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { RouterLink } from 'vue-router'
import LangSwitch from './LangSwitch.vue'
import { siteNav } from '@/config/siteNav'

const { t } = useI18n()
const scrolled = ref(false)

function onScroll() {
  scrolled.value = window.scrollY > 40
}

onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<template>
  <nav
    class="fixed top-0 left-0 right-0 z-50 transition-all duration-500"
    :class="scrolled ? 'py-3 bg-bg/90 backdrop-blur-md border-b border-line' : 'py-5'"
  >
    <div class="max-w-6xl mx-auto px-6 flex items-center justify-between gap-4">
      <RouterLink to="/" class="font-display text-xl tracking-wide text-ink shrink-0">
        知墨
      </RouterLink>

      <div class="flex items-center gap-5 md:gap-7 overflow-x-auto max-w-[50vw] md:max-w-none scrollbar-none">
        <RouterLink
          v-for="item in siteNav"
          :key="item.path"
          :to="item.path"
          class="text-sm text-ink-muted hover:text-ink transition-colors tracking-wide whitespace-nowrap shrink-0"
          active-class="!text-ink"
        >
          {{ t(item.labelKey) }}
        </RouterLink>
      </div>

      <div class="flex items-center gap-3 shrink-0">
        <LangSwitch />
        <RouterLink
          to="/admin"
          class="hidden sm:inline-flex text-xs px-4 py-2 border border-line text-ink-muted hover:text-ink hover:border-ink-muted transition-all tracking-wide"
        >
          {{ t('nav.admin') }}
        </RouterLink>
      </div>
    </div>
  </nav>
</template>
