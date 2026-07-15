<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { adminApi, setAuthToken } from '@/api'
import { useAuthStore } from '@/stores'

const { t } = useI18n()
const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    const { data } = await adminApi.login(username.value, password.value)
    setAuthToken(data.access_token)
    authStore.setToken(data.access_token)
    router.push('/admin')
  } catch {
    error.value = t('admin.login_error')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center px-6">
    <div class="washi-panel w-full max-w-md p-8">
      <h1 class="font-display font-semibold text-2xl mb-8 text-center tracking-wide text-ink">Admin</h1>

      <form class="space-y-4" @submit.prevent="handleLogin">
        <div>
          <label class="block text-sm text-ink-muted mb-2 tracking-wide">{{ t('admin.username') }}</label>
          <input
            v-model="username"
            type="text"
            required
            class="w-full px-4 py-3 bg-surface border border-line focus:border-accent outline-none transition-colors"
          />
        </div>
        <div>
          <label class="block text-sm text-ink-muted mb-2 tracking-wide">{{ t('admin.password') }}</label>
          <input
            v-model="password"
            type="password"
            required
            class="w-full px-4 py-3 bg-surface border border-line focus:border-accent outline-none transition-colors"
          />
        </div>

        <p v-if="error" class="text-red-700/80 text-sm">{{ error }}</p>

        <button
          type="submit"
          :disabled="loading"
          class="w-full btn-primary disabled:opacity-50"
        >
          {{ t('admin.login') }}
        </button>
      </form>

      <router-link to="/" class="block text-center text-sm text-ink-faint mt-6 hover:text-ink tracking-wide">
        ← {{ t('admin.back') }}
      </router-link>
    </div>
  </div>
</template>
