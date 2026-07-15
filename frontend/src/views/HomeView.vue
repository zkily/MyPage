<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { RouterLink } from 'vue-router'
import HeroSection from '@/components/hero/HeroSection.vue'
import CoverImageMarquee from '@/components/hero/CoverImageMarquee.vue'
import { siteNav } from '@/config/siteNav'

const { t } = useI18n()

const explore = siteNav.filter((item) => item.name !== 'contact')
</script>

<template>
  <div>
    <HeroSection />
    <CoverImageMarquee />

    <section class="py-20 px-6 border-t border-line">
      <div class="max-w-6xl mx-auto">
        <p class="text-xs text-ink-faint tracking-[0.3em] mb-8">{{ t('home.explore') }}</p>
        <ul class="grid sm:grid-cols-2 lg:grid-cols-4 gap-x-8 gap-y-6">
          <li v-for="item in explore" :key="item.path">
            <RouterLink
              :to="item.path"
              class="group block border-b border-line pb-4 hover:border-ink-muted transition-colors"
            >
              <span class="font-display text-xl text-ink tracking-wide group-hover:text-accent transition-colors">
                {{ t(item.labelKey) }}
              </span>
              <span class="block mt-2 text-sm text-ink-faint group-hover:text-ink-muted transition-colors">
                {{ t(`home.teaser.${item.name}`) }} →
              </span>
            </RouterLink>
          </li>
        </ul>
      </div>
    </section>
  </div>
</template>
