<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores'
import LangSwitch from '@/components/layout/LangSwitch.vue'

const { t } = useI18n()
const router = useRouter()
const authStore = useAuthStore()

function logout() {
  authStore.logout()
  router.push('/admin/login')
}
</script>

<template>
  <div class="min-h-screen flex">
    <aside class="w-64 bg-surface border-r border-line p-6 flex flex-col">
      <h1 class="font-display font-semibold text-xl mb-8 tracking-wide text-ink">
        Admin
      </h1>

      <nav class="space-y-1 flex-1">
        <router-link
          to="/admin"
          class="block px-4 py-2 text-sm text-ink-muted hover:bg-surface-hover hover:text-ink transition-colors tracking-wide"
          active-class="!bg-surface-hover !text-ink"
        >
          {{ t('admin.dashboard') }}
        </router-link>
        <router-link
          to="/admin/projects"
          class="block px-4 py-2 text-sm text-ink-muted hover:bg-surface-hover hover:text-ink transition-colors tracking-wide"
          active-class="!bg-surface-hover !text-ink"
        >
          {{ t('admin.projects') }}
        </router-link>
        <router-link
          to="/admin/knowledge"
          class="block px-4 py-2 text-sm text-ink-muted hover:bg-surface-hover hover:text-ink transition-colors tracking-wide"
          active-class="!bg-surface-hover !text-ink"
        >
          {{ t('admin.knowledge') }}
        </router-link>
      </nav>

      <div class="space-y-4 pt-4 border-t border-line">
        <LangSwitch />
        <button
          class="w-full px-4 py-2 text-sm text-ink-faint hover:text-ink transition-colors text-left tracking-wide"
          @click="logout"
        >
          {{ t('admin.logout') }}
        </button>
        <router-link to="/" class="block text-sm text-ink-faint hover:text-ink tracking-wide">
          ← {{ t('admin.back') }}
        </router-link>
      </div>
    </aside>

    <main class="flex-1 p-8 overflow-y-auto">
      <router-view />
    </main>
  </div>
</template>
