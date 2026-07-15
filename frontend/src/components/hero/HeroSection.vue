<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import ParticleBg from './ParticleBg.vue'
import InkLandscape from './InkLandscape.vue'
import { RouterLink } from 'vue-router'

const { t } = useI18n()
</script>

<template>
  <section id="home" class="relative min-h-screen flex items-end md:items-center overflow-hidden">
    <InkLandscape />
    <ParticleBg />

    <div
      class="absolute inset-0 pointer-events-none"
      aria-hidden="true"
      style="
        background: linear-gradient(
          100deg,
          rgba(235, 232, 226, 0.94) 0%,
          rgba(235, 232, 226, 0.72) 32%,
          rgba(235, 232, 226, 0.28) 55%,
          transparent 72%
        );
      "
    />

    <div class="relative z-10 w-full max-w-6xl mx-auto px-6 pb-24 pt-32 md:py-0">
      <p
        v-motion
        :initial="{ opacity: 0, y: 12 }"
        :enter="{ opacity: 1, y: 0, transition: { delay: 120, duration: 700 } }"
        class="font-display text-ink-faint text-sm tracking-[0.35em] mb-8"
      >
        {{ t('hero.greeting') }}
      </p>

      <div class="flex items-end gap-5 mb-4">
        <h1
          v-motion
          :initial="{ opacity: 0, y: 20 }"
          :enter="{ opacity: 1, y: 0, transition: { delay: 280, duration: 800 } }"
          class="font-display font-semibold text-5xl sm:text-7xl md:text-8xl tracking-wide text-ink leading-[1.05]"
        >
          知墨
        </h1>
        <span
          v-motion
          :initial="{ opacity: 0, scale: 0.85 }"
          :enter="{ opacity: 1, scale: 1, transition: { delay: 900, duration: 600 } }"
          class="seal mb-2 hidden sm:inline-flex"
          aria-hidden="true"
        >
          知
        </span>
      </div>

      <p
        v-motion
        :initial="{ opacity: 0, y: 14 }"
        :enter="{ opacity: 1, y: 0, transition: { delay: 420, duration: 700 } }"
        class="font-display text-2xl sm:text-3xl text-accent mb-6 tracking-wide"
      >
        {{ t('hero.role') }}
      </p>

      <p
        v-motion
        :initial="{ opacity: 0, y: 12 }"
        :enter="{ opacity: 1, y: 0, transition: { delay: 560, duration: 700 } }"
        class="text-ink-muted text-base md:text-lg max-w-md mb-12 leading-relaxed"
      >
        {{ t('hero.subtitle') }}
      </p>

      <div
        v-motion
        :initial="{ opacity: 0, y: 12 }"
        :enter="{ opacity: 1, y: 0, transition: { delay: 700, duration: 700 } }"
        class="flex flex-wrap gap-3"
      >
        <RouterLink to="/projects" class="btn-primary">
          {{ t('hero.cta_projects') }}
        </RouterLink>
        <RouterLink to="/contact" class="btn-ghost">
          {{ t('hero.cta_contact') }}
        </RouterLink>
      </div>
    </div>

    <div
      v-motion
      :initial="{ opacity: 0 }"
      :enter="{ opacity: 1, transition: { delay: 1000, duration: 900 } }"
      class="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 text-ink-faint z-10"
    >
      <span class="w-px h-8 bg-line block origin-top animate-[grow_2.4s_ease-in-out_infinite]" />
    </div>
  </section>
</template>

<style scoped>
@keyframes grow {
  0%,
  100% {
    transform: scaleY(0.45);
    opacity: 0.35;
  }
  50% {
    transform: scaleY(1);
    opacity: 0.85;
  }
}

.seal {
  width: 2.1rem;
  height: 2.1rem;
  align-items: center;
  justify-content: center;
  font-family: "Noto Serif SC", "Shippori Mincho", serif;
  font-size: 0.95rem;
  font-weight: 600;
  color: #8b3a3a;
  border: 1.5px solid #8b3a3a;
  letter-spacing: 0;
  line-height: 1;
  opacity: 0.72;
}
</style>
