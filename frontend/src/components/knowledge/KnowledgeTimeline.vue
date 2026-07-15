<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import MarkdownIt from 'markdown-it'
import { publicApi } from '@/api'
import { useLocaleStore } from '@/stores'
import type { KnowledgeArticle, KnowledgeListItem } from '@/types'
import ArticleCard from './ArticleCard.vue'

const { t } = useI18n()
const localeStore = useLocaleStore()
const articles = ref<KnowledgeListItem[]>([])
const loading = ref(true)
const selected = ref<KnowledgeArticle | null>(null)
const sectionRef = ref<HTMLElement | null>(null)
const visible = ref(false)

const md = new MarkdownIt({ html: true, linkify: true })

async function fetchArticles() {
  loading.value = true
  try {
    const { data } = await publicApi.getKnowledge(localeStore.currentLang)
    articles.value = data
  } catch {
    articles.value = []
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await fetchArticles()

  const observer = new IntersectionObserver(
    ([entry]) => {
      if (entry.isIntersecting) visible.value = true
    },
    { threshold: 0.1 },
  )
  if (sectionRef.value) observer.observe(sectionRef.value)
})

watch(() => localeStore.currentLang, fetchArticles)

async function openArticle(article: KnowledgeListItem) {
  try {
    const { data } = await publicApi.getKnowledgeArticle(article.slug, localeStore.currentLang)
    selected.value = data
  } catch {
    selected.value = null
  }
}

function closeModal() {
  selected.value = null
}
</script>

<template>
  <section id="knowledge" ref="sectionRef" class="py-24 px-6 shan-shui-wash">
    <div class="max-w-3xl mx-auto">
      <div class="reveal-up mb-16 section-rule" :class="{ visible }">
        <h2 class="font-display font-semibold text-3xl md:text-4xl text-ink tracking-wide mb-3">
          {{ t('knowledge.title') }}
        </h2>
        <p class="text-ink-muted text-base">{{ t('knowledge.subtitle') }}</p>
      </div>

      <div v-if="loading" class="text-center text-ink-faint py-20 tracking-wide">Loading...</div>

      <div v-else-if="articles.length === 0" class="text-center text-ink-faint py-20 tracking-wide">
        {{ t('knowledge.empty') }}
      </div>

      <div v-else class="relative">
        <ArticleCard
          v-for="(article, index) in articles"
          :key="article.id"
          :article="article"
          :index="index"
          @click="openArticle"
        />
      </div>
    </div>

    <Teleport to="body">
      <Transition name="modal">
        <div
          v-if="selected"
          class="fixed inset-0 z-[100] flex items-center justify-center p-6 bg-ink/40 backdrop-blur-sm"
          @click.self="closeModal"
        >
          <div class="washi-panel max-w-3xl w-full max-h-[85vh] overflow-y-auto p-8">
            <span
              v-if="selected.category"
              class="inline-block text-xs px-2.5 py-1 border border-line text-accent mb-4 tracking-wide"
            >
              {{ selected.category }}
            </span>
            <h3 class="font-display font-semibold text-2xl mb-6 text-ink tracking-wide">{{ selected.title }}</h3>
            <div
              class="prose prose-stone prose-sm max-w-none text-ink-muted"
              v-html="md.render(selected.content)"
            />
            <button
              class="mt-8 btn-ghost text-sm"
              @click="closeModal"
            >
              {{ t('knowledge.close') }}
            </button>
          </div>
        </div>
      </Transition>
    </Teleport>
  </section>
</template>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>
