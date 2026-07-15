<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { RouterLink } from 'vue-router'

const { t, tm } = useI18n()
const sectionRef = ref<HTMLElement | null>(null)
const visible = ref(false)

const paths = [
  { to: '/projects', key: 'works' },
  { to: '/records', key: 'life' },
  { to: '/knowledge', key: 'share' },
] as const

const interests = computed(() => {
  const items = tm('about.interests.items')
  return Array.isArray(items) ? (items as { title: string; text: string }[]) : []
})

onMounted(() => {
  const observer = new IntersectionObserver(
    ([entry]) => {
      if (entry.isIntersecting) visible.value = true
    },
    { threshold: 0.1 },
  )
  if (sectionRef.value) observer.observe(sectionRef.value)
})
</script>

<template>
  <div ref="sectionRef" class="pt-8 pb-8">
    <!-- 自我介绍 -->
    <section class="px-6 py-16 md:py-20 shan-shui-wash">
      <div class="max-w-6xl mx-auto grid md:grid-cols-12 gap-12 md:gap-16 items-start">
        <div class="md:col-span-5 reveal-up" :class="{ visible }">
          <h1 class="font-display font-semibold text-3xl md:text-4xl text-ink tracking-wide mb-3 section-rule">
            {{ t('about.title') }}
          </h1>
          <p class="text-ink-muted text-base mt-6 leading-relaxed">{{ t('about.subtitle') }}</p>
          <p class="font-display text-accent text-xl tracking-wide mt-8">{{ t('about.role') }}</p>
        </div>

        <div class="md:col-span-7 reveal-up space-y-5" :class="{ visible }" style="transition-delay: 100ms">
          <p class="text-ink text-lg leading-relaxed tracking-wide">
            {{ t('about.p1') }}
          </p>
          <p class="text-ink-muted leading-relaxed">
            {{ t('about.p2') }}
          </p>
          <p class="text-ink-muted leading-relaxed">
            {{ t('about.p3') }}
          </p>
        </div>
      </div>
    </section>

    <!-- 三件事：作品 / 生活 / 分享 -->
    <section class="px-6 py-16 border-t border-line">
      <div class="max-w-6xl mx-auto">
        <p class="text-xs text-ink-faint tracking-[0.3em] mb-3">{{ t('about.paths_label') }}</p>
        <h2 class="font-display text-2xl md:text-3xl text-ink tracking-wide mb-4">
          {{ t('about.paths_title') }}
        </h2>
        <p class="text-ink-muted text-sm mb-12 max-w-xl leading-relaxed">
          {{ t('about.paths_subtitle') }}
        </p>

        <ul class="grid md:grid-cols-3 gap-x-10 gap-y-10">
          <li v-for="(path, i) in paths" :key="path.key">
            <RouterLink :to="path.to" class="group block border-t border-line pt-6 h-full">
              <span class="font-display text-accent text-sm tracking-wide">
                {{ String(i + 1).padStart(2, '0') }}
              </span>
              <h3 class="font-display text-xl text-ink tracking-wide mt-3 mb-3 group-hover:text-accent transition-colors">
                {{ t(`about.paths.${path.key}.title`) }}
              </h3>
              <p class="text-sm text-ink-muted leading-relaxed mb-4">
                {{ t(`about.paths.${path.key}.text`) }}
              </p>
              <span class="text-sm text-accent tracking-wide">
                {{ t(`about.paths.${path.key}.cta`) }} →
              </span>
            </RouterLink>
          </li>
        </ul>
      </div>
    </section>

    <!-- 兴趣：烹饪 / 旅游 / 音乐 -->
    <section class="px-6 py-16 border-t border-line shan-shui-wash">
      <div class="max-w-6xl mx-auto grid md:grid-cols-12 gap-12">
        <div class="md:col-span-4">
          <p class="text-xs text-ink-faint tracking-[0.3em] mb-3">{{ t('about.interests.label') }}</p>
          <h2 class="font-display text-2xl md:text-3xl text-ink tracking-wide mb-4">
            {{ t('about.interests.title') }}
          </h2>
          <p class="text-ink-muted text-sm leading-relaxed">
            {{ t('about.interests.subtitle') }}
          </p>
        </div>

        <ul class="md:col-span-8 space-y-8">
          <li
            v-for="(item, i) in interests"
            :key="i"
            class="grid sm:grid-cols-12 gap-3 sm:gap-6 items-start border-b border-line pb-8 last:border-0 last:pb-0"
          >
            <span class="sm:col-span-3 font-display text-ink tracking-wide">
              {{ item.title }}
            </span>
            <p class="sm:col-span-9 text-ink-muted text-sm leading-relaxed">
              {{ item.text }}
            </p>
          </li>
        </ul>
      </div>
    </section>

    <!-- 邀请 -->
    <section class="px-6 py-16 border-t border-line">
      <div class="max-w-3xl mx-auto text-center">
        <p class="font-display text-xl md:text-2xl text-ink tracking-wide mb-4 leading-relaxed">
          {{ t('about.invite') }}
        </p>
        <p class="text-ink-muted text-sm mb-8 leading-relaxed">
          {{ t('about.invite_sub') }}
        </p>
        <div class="flex flex-wrap gap-3 justify-center">
          <RouterLink to="/knowledge" class="btn-primary">{{ t('about.cta_knowledge') }}</RouterLink>
          <RouterLink to="/contact" class="btn-ghost">{{ t('about.cta_contact') }}</RouterLink>
        </div>
      </div>
    </section>
  </div>
</template>
