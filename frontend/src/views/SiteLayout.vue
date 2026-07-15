<script setup lang="ts">
import { RouterView } from 'vue-router'
import NavBar from '@/components/layout/NavBar.vue'
import SiteFooter from '@/components/layout/SiteFooter.vue'
import InkWashBg from '@/components/fx/InkWashBg.vue'
</script>

<template>
  <div class="relative min-h-screen">
    <InkWashBg />
    <div class="relative z-10 min-h-screen flex flex-col">
      <NavBar />
      <main class="flex-1">
        <RouterView />
      </main>
      <SiteFooter />
    </div>
  </div>
</template>
