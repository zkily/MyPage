import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import type { LangCode } from '@/types'

export const useLocaleStore = defineStore('locale', () => {
  const { locale } = useI18n()

  const currentLang = computed(() => locale.value as LangCode)

  function setLang(lang: LangCode) {
    locale.value = lang
    localStorage.setItem('locale', lang)
    document.documentElement.lang = lang === 'zh' ? 'zh-CN' : lang
  }

  return { currentLang, setLang }
})

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('admin_token'))

  const isAuthenticated = computed(() => !!token.value)

  function setToken(t: string | null) {
    token.value = t
    if (t) {
      localStorage.setItem('admin_token', t)
    } else {
      localStorage.removeItem('admin_token')
    }
  }

  function logout() {
    setToken(null)
  }

  return { token, isAuthenticated, setToken, logout }
})
