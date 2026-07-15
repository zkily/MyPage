<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import MarkdownIt from 'markdown-it'
import { publicApi } from '@/api'
import { useLocaleStore } from '@/stores'
import {
  articleMatchesSection,
  knowledgeSections,
  type KnowledgeSection,
} from '@/config/knowledgeMenu'
import type { KnowledgeArticle, KnowledgeListItem } from '@/types'

const { t } = useI18n()
const localeStore = useLocaleStore()

const articles = ref<KnowledgeListItem[]>([])
const loading = ref(true)
const activeSectionId = ref(knowledgeSections[0]?.id ?? 'all')
const selectedSlug = ref<string | null>(null)
const detail = ref<KnowledgeArticle | null>(null)
const detailLoading = ref(false)
const mobileMenuOpen = ref(false)

const md = new MarkdownIt({ html: true, linkify: true })

const activeSection = computed(
  () => knowledgeSections.find((s) => s.id === activeSectionId.value) ?? knowledgeSections[0],
)

const filteredArticles = computed(() => {
  const section = activeSection.value
  if (!section) return articles.value
  return articles.value.filter((a) => articleMatchesSection(a, section))
})

async function fetchArticles() {
  loading.value = true
  try {
    const { data } = await publicApi.getKnowledge(localeStore.currentLang)
    articles.value = data
    if (selectedSlug.value && !data.some((a: KnowledgeListItem) => a.slug === selectedSlug.value)) {
      selectedSlug.value = null
      detail.value = null
    }
  } catch {
    articles.value = []
  } finally {
    loading.value = false
  }
}

async function loadDetail(slug: string) {
  selectedSlug.value = slug
  detailLoading.value = true
  mobileMenuOpen.value = false
  try {
    const { data } = await publicApi.getKnowledgeArticle(slug, localeStore.currentLang)
    detail.value = data
  } catch {
    detail.value = null
  } finally {
    detailLoading.value = false
  }
}

function selectSection(section: KnowledgeSection) {
  activeSectionId.value = section.id
  selectedSlug.value = null
  detail.value = null
  mobileMenuOpen.value = false
}

function formatDate(date: string | null) {
  if (!date) return ''
  return new Date(date).toLocaleDateString()
}

onMounted(fetchArticles)
watch(() => localeStore.currentLang, async () => {
  await fetchArticles()
  if (selectedSlug.value) await loadDetail(selectedSlug.value)
})
</script>

<template>
  <section class="pt-28 pb-16 px-4 sm:px-6 min-h-[calc(100vh-4rem)]">
    <div class="max-w-6xl mx-auto mb-8 md:mb-10">
      <h1 class="font-display font-semibold text-3xl md:text-4xl text-ink tracking-wide mb-3 section-rule">
        {{ t('knowledge.title') }}
      </h1>
      <p class="text-ink-muted text-base mt-6">{{ t('knowledge.subtitle') }}</p>
    </div>

    <!-- 移动端：打开菜单 -->
    <div class="md:hidden max-w-6xl mx-auto mb-4">
      <button
        type="button"
        class="btn-ghost text-sm w-full justify-between"
        @click="mobileMenuOpen = !mobileMenuOpen"
      >
        <span>{{ t(`knowledge.sections.${activeSectionId}`) }}</span>
        <span class="text-ink-faint">{{ mobileMenuOpen ? '▲' : '▼' }}</span>
      </button>
    </div>

    <div class="max-w-6xl mx-auto flex flex-col md:flex-row gap-0 md:gap-10 md:items-start border border-line bg-surface/40">
      <!-- 左侧菜单 -->
      <aside
        class="md:w-64 shrink-0 border-b md:border-b-0 md:border-r border-line"
        :class="mobileMenuOpen ? 'block' : 'hidden md:block'"
      >
        <div class="p-5 md:p-6 md:sticky md:top-24 md:max-h-[calc(100vh-7rem)] md:overflow-y-auto">
          <p class="text-xs text-ink-faint tracking-[0.25em] mb-4">
            {{ t('knowledge.menu_title') }}
          </p>

          <nav class="space-y-1 mb-8">
            <button
              v-for="section in knowledgeSections"
              :key="section.id"
              type="button"
              class="w-full text-left px-3 py-2.5 text-sm tracking-wide transition-colors border-l-2"
              :class="
                activeSectionId === section.id
                  ? 'border-accent text-ink bg-surface-hover/60'
                  : 'border-transparent text-ink-muted hover:text-ink hover:bg-surface-hover/40'
              "
              @click="selectSection(section)"
            >
              {{ t(`knowledge.sections.${section.id}`) }}
            </button>
          </nav>

          <p class="text-xs text-ink-faint tracking-[0.25em] mb-3">
            {{ t('knowledge.article_list') }}
          </p>

          <div v-if="loading" class="text-xs text-ink-faint py-4">Loading...</div>
          <ul v-else-if="filteredArticles.length" class="space-y-1">
            <li v-for="article in filteredArticles" :key="article.id">
              <button
                type="button"
                class="w-full text-left px-3 py-2 text-sm tracking-wide transition-colors"
                :class="
                  selectedSlug === article.slug
                    ? 'text-accent'
                    : 'text-ink-muted hover:text-ink'
                "
                @click="loadDetail(article.slug)"
              >
                <span class="line-clamp-2">{{ article.title }}</span>
              </button>
            </li>
          </ul>
          <p v-else class="text-xs text-ink-faint px-3 py-2 leading-relaxed">
            {{ t('knowledge.section_empty') }}
          </p>
        </div>
      </aside>

      <!-- 右侧内容 -->
      <div class="flex-1 min-w-0 p-6 md:p-10 min-h-[28rem]">
        <!-- 未选文章：板块概览 + 列表 -->
        <template v-if="!selectedSlug">
          <h2 class="font-display text-2xl text-ink tracking-wide mb-2">
            {{ t(`knowledge.sections.${activeSectionId}`) }}
          </h2>
          <p class="text-ink-muted text-sm mb-10 leading-relaxed">
            {{ t(`knowledge.section_desc.${activeSectionId}`) }}
          </p>

          <div v-if="loading" class="text-ink-faint tracking-wide py-12">Loading...</div>

          <div v-else-if="filteredArticles.length === 0" class="text-ink-faint tracking-wide py-12">
            {{ t('knowledge.section_empty') }}
          </div>

          <ul v-else class="space-y-0 divide-y divide-line border-t border-line">
            <li
              v-for="article in filteredArticles"
              :key="article.id"
            >
              <button
                type="button"
                class="w-full text-left py-6 group hover:bg-surface-hover/30 transition-colors -mx-2 px-2"
                @click="loadDetail(article.slug)"
              >
                <div class="flex flex-wrap items-baseline gap-3 mb-2">
                  <time v-if="article.published_at" class="text-xs text-ink-faint tracking-wide">
                    {{ formatDate(article.published_at) }}
                  </time>
                  <span
                    v-if="article.category"
                    class="text-xs text-accent tracking-wide"
                  >
                    {{ article.category }}
                  </span>
                </div>
                <h3 class="font-display text-lg text-ink group-hover:text-accent transition-colors tracking-wide mb-2">
                  {{ article.title }}
                </h3>
                <p class="text-sm text-ink-muted line-clamp-2 leading-relaxed">
                  {{ article.summary }}
                </p>
                <span class="inline-block mt-3 text-sm text-accent tracking-wide">
                  {{ t('knowledge.readMore') }} →
                </span>
              </button>
            </li>
          </ul>
        </template>

        <!-- 已选文章：正文 -->
        <template v-else>
          <button
            type="button"
            class="text-sm text-ink-faint hover:text-ink tracking-wide mb-8 transition-colors"
            @click="selectedSlug = null; detail = null"
          >
            ← {{ t('knowledge.back_list') }}
          </button>

          <div v-if="detailLoading" class="text-ink-faint tracking-wide py-12">Loading...</div>

          <article v-else-if="detail">
            <span
              v-if="detail.category"
              class="inline-block text-xs px-2.5 py-1 border border-line text-accent mb-4 tracking-wide"
            >
              {{ detail.category }}
            </span>
            <h2 class="font-display font-semibold text-2xl md:text-3xl text-ink tracking-wide mb-4">
              {{ detail.title }}
            </h2>
            <time
              v-if="detail.published_at"
              class="block text-xs text-ink-faint tracking-wide mb-8"
            >
              {{ formatDate(detail.published_at) }}
            </time>
            <div
              class="prose prose-stone prose-sm md:prose-base max-w-none text-ink-muted"
              v-html="md.render(detail.content)"
            />
            <div v-if="detail.tags?.length" class="flex flex-wrap gap-2 mt-10 pt-6 border-t border-line">
              <span
                v-for="tag in detail.tags"
                :key="tag"
                class="text-xs text-ink-faint tracking-wide"
              >
                #{{ tag }}
              </span>
            </div>
          </article>

          <p v-else class="text-ink-faint tracking-wide py-12">{{ t('knowledge.empty') }}</p>
        </template>
      </div>
    </div>
  </section>
</template>
