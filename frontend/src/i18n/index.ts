import { createI18n } from 'vue-i18n'
import ja from './ja.json'
import zh from './zh.json'
import en from './en.json'
import type { LangCode } from '@/types'

const saved = localStorage.getItem('locale') as LangCode | null
const defaultLocale: LangCode = saved && ['ja', 'zh', 'en'].includes(saved) ? saved : 'ja'

export const i18n = createI18n({
  legacy: false,
  locale: defaultLocale,
  fallbackLocale: 'ja',
  messages: { ja, zh, en },
})

export function setLocale(locale: LangCode) {
  i18n.global.locale.value = locale
  localStorage.setItem('locale', locale)
  document.documentElement.lang = locale === 'zh' ? 'zh-CN' : locale
}
