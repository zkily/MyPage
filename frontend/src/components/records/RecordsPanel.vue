<script setup lang="ts">
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import {
  recordMatchesSection,
  recordsItems,
  recordsSections,
  type RecordsItem,
  type RecordsSection,
} from '@/config/recordsMenu'

const { t } = useI18n()

const activeSectionId = ref(recordsSections[0]?.id ?? 'all')
const selectedId = ref<string | null>(null)
const mobileMenuOpen = ref(false)

const filteredItems = computed(() =>
  recordsItems.filter((item) => recordMatchesSection(item, activeSectionId.value)),
)

const selected = computed(
  () => recordsItems.find((item) => item.id === selectedId.value) ?? null,
)

function selectSection(section: RecordsSection) {
  activeSectionId.value = section.id
  selectedId.value = null
  mobileMenuOpen.value = false
}

function openItem(item: RecordsItem) {
  selectedId.value = item.id
  mobileMenuOpen.value = false
}

function formatDate(date?: string) {
  if (!date) return ''
  return new Date(date).toLocaleDateString()
}
</script>

<template>
  <section class="pt-28 pb-16 px-4 sm:px-6 min-h-[calc(100vh-4rem)]">
    <div class="max-w-6xl mx-auto mb-8 md:mb-10">
      <h1 class="font-display font-semibold text-3xl md:text-4xl text-ink tracking-wide mb-3 section-rule">
        {{ t('records.title') }}
      </h1>
      <p class="text-ink-muted text-base mt-6">{{ t('records.subtitle') }}</p>
    </div>

    <div class="md:hidden max-w-6xl mx-auto mb-4">
      <button
        type="button"
        class="btn-ghost text-sm w-full justify-between"
        @click="mobileMenuOpen = !mobileMenuOpen"
      >
        <span>{{ t(`records.sections.${activeSectionId}`) }}</span>
        <span class="text-ink-faint">{{ mobileMenuOpen ? '▲' : '▼' }}</span>
      </button>
    </div>

    <div class="max-w-6xl mx-auto flex flex-col md:flex-row gap-0 md:gap-10 md:items-start border border-line bg-surface/40">
      <aside
        class="md:w-64 shrink-0 border-b md:border-b-0 md:border-r border-line"
        :class="mobileMenuOpen ? 'block' : 'hidden md:block'"
      >
        <div class="p-5 md:p-6 md:sticky md:top-24 md:max-h-[calc(100vh-7rem)] md:overflow-y-auto">
          <p class="text-xs text-ink-faint tracking-[0.25em] mb-4">
            {{ t('records.menu_title') }}
          </p>

          <nav class="space-y-1 mb-8">
            <button
              v-for="section in recordsSections"
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
              {{ t(`records.sections.${section.id}`) }}
            </button>
          </nav>

          <p class="text-xs text-ink-faint tracking-[0.25em] mb-3">
            {{ t('records.item_list') }}
          </p>

          <ul v-if="filteredItems.length" class="space-y-1">
            <li v-for="item in filteredItems" :key="item.id">
              <button
                type="button"
                class="w-full text-left px-3 py-2 text-sm tracking-wide transition-colors"
                :class="selectedId === item.id ? 'text-accent' : 'text-ink-muted hover:text-ink'"
                @click="openItem(item)"
              >
                <span class="line-clamp-2">{{ t(`records.items.${item.titleKey}`) }}</span>
              </button>
            </li>
          </ul>
          <p v-else class="text-xs text-ink-faint px-3 py-2 leading-relaxed">
            {{ t('records.section_empty') }}
          </p>
        </div>
      </aside>

      <div class="flex-1 min-w-0 p-6 md:p-10 min-h-[28rem]">
        <template v-if="!selected">
          <h2 class="font-display text-2xl text-ink tracking-wide mb-2">
            {{ t(`records.sections.${activeSectionId}`) }}
          </h2>
          <p class="text-ink-muted text-sm mb-10 leading-relaxed">
            {{ t(`records.section_desc.${activeSectionId}`) }}
          </p>

          <div v-if="filteredItems.length === 0" class="text-ink-faint tracking-wide py-12">
            {{ t('records.section_empty') }}
          </div>

          <ul v-else class="space-y-0 divide-y divide-line border-t border-line">
            <li v-for="item in filteredItems" :key="item.id">
              <button
                type="button"
                class="w-full text-left py-6 group hover:bg-surface-hover/30 transition-colors -mx-2 px-2"
                @click="openItem(item)"
              >
                <time v-if="item.date" class="block text-xs text-ink-faint tracking-wide mb-2">
                  {{ formatDate(item.date) }}
                </time>
                <h3 class="font-display text-lg text-ink group-hover:text-accent transition-colors tracking-wide mb-2">
                  {{ t(`records.items.${item.titleKey}`) }}
                </h3>
                <p class="text-sm text-ink-muted line-clamp-2 leading-relaxed">
                  {{ t(`records.items.${item.summaryKey}`) }}
                </p>
                <span class="inline-block mt-3 text-sm text-accent tracking-wide">
                  {{ t('records.readMore') }} →
                </span>
              </button>
            </li>
          </ul>
        </template>

        <template v-else>
          <button
            type="button"
            class="text-sm text-ink-faint hover:text-ink tracking-wide mb-8 transition-colors"
            @click="selectedId = null"
          >
            ← {{ t('records.back_list') }}
          </button>

          <article>
            <time v-if="selected.date" class="block text-xs text-ink-faint tracking-wide mb-4">
              {{ formatDate(selected.date) }}
            </time>
            <h2 class="font-display font-semibold text-2xl md:text-3xl text-ink tracking-wide mb-6">
              {{ t(`records.items.${selected.titleKey}`) }}
            </h2>
            <div class="text-ink-muted leading-relaxed whitespace-pre-line">
              {{ t(`records.items.${selected.contentKey}`) }}
            </div>
          </article>
        </template>
      </div>
    </div>
  </section>
</template>
