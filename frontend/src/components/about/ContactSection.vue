<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const sectionRef = ref<HTMLElement | null>(null)
const visible = ref(false)

/** 邮箱不放进 i18n，避免 @ 被 vue-i18n 当成链接语法 */
const email = 'hello@zhimo.example'

/** 以后换成真实二维码图片路径，例如 /qr.png */
const qrSrc = ''

onMounted(() => {
  const observer = new IntersectionObserver(
    ([entry]) => {
      if (entry.isIntersecting) visible.value = true
    },
    { threshold: 0.15 },
  )
  if (sectionRef.value) observer.observe(sectionRef.value)
})
</script>

<template>
  <section id="contact" ref="sectionRef" class="py-24 px-6">
    <div class="max-w-3xl mx-auto reveal-up" :class="{ visible }">
      <h2 class="font-display font-semibold text-3xl md:text-4xl text-ink tracking-wide mb-3 section-rule">
        {{ t('contact.title') }}
      </h2>
      <p class="text-ink-muted text-base mt-6 mb-14 max-w-xl leading-relaxed">
        {{ t('contact.subtitle') }}
      </p>

      <div class="grid sm:grid-cols-2 gap-12 items-start">
        <div>
          <p class="text-xs text-ink-faint tracking-[0.25em] mb-3">{{ t('contact.email_label') }}</p>
          <a
            :href="`mailto:${email}`"
            class="font-display text-xl md:text-2xl text-ink hover:text-accent transition-colors tracking-wide break-all"
          >
            {{ email }}
          </a>
          <a :href="`mailto:${email}`" class="btn-primary inline-flex mt-8">
            {{ t('contact.cta') }}
          </a>
        </div>

        <div>
          <p class="text-xs text-ink-faint tracking-[0.25em] mb-3">{{ t('contact.qr_label') }}</p>
          <div
            class="w-40 h-40 border border-line bg-surface flex items-center justify-center"
          >
            <img
              v-if="qrSrc"
              :src="qrSrc"
              :alt="t('contact.qr_label')"
              class="w-full h-full object-contain p-2"
            />
            <p v-else class="text-xs text-ink-faint tracking-wide text-center px-4 leading-relaxed">
              {{ t('contact.qr_placeholder') }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
