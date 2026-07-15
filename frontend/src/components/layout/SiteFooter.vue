<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { RouterLink } from 'vue-router'

const { t } = useI18n()
const email = 'hello@zhimo.example'
</script>

<template>
  <footer class="py-14 px-6 border-t border-line">
    <div class="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
      <div class="text-center md:text-left">
        <RouterLink to="/" class="font-display text-lg tracking-wide text-ink">知墨</RouterLink>
        <p class="text-ink-faint text-xs tracking-wide mt-1">{{ t('footer.tagline') }}</p>
      </div>

      <p class="text-ink-faint text-sm tracking-wide text-center max-w-md leading-relaxed">
        {{ t('footer.copyright') }}
      </p>

      <div class="flex flex-col sm:flex-row items-center gap-4 text-sm">
        <a
          :href="`mailto:${email}`"
          class="text-ink-faint hover:text-accent transition-colors tracking-wide"
        >
          {{ t('footer.email') }}
        </a>
        <RouterLink
          to="/contact"
          class="text-ink-faint hover:text-accent transition-colors tracking-wide"
        >
          {{ t('footer.qr') }}
        </RouterLink>
      </div>
    </div>
  </footer>
</template>
