<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'

/** 墨点与飞白：缓慢飘散，似山水画中的雨雾 */
const canvasRef = ref<HTMLCanvasElement | null>(null)

let animationId = 0
let onResize: (() => void) | null = null

function startMist(el: HTMLCanvasElement) {
  const ctx = el.getContext('2d')
  if (!ctx) return
  const g: CanvasRenderingContext2D = ctx

  type Dot = { x: number; y: number; vx: number; vy: number; r: number; a: number; soft: boolean }
  const dots: Dot[] = []
  const count = 48

  function resize() {
    el.width = window.innerWidth
    el.height = window.innerHeight
  }

  function init() {
    dots.length = 0
    for (let i = 0; i < count; i++) {
      dots.push({
        x: Math.random() * el.width,
        y: Math.random() * el.height,
        vx: (Math.random() - 0.3) * 0.22,
        vy: (Math.random() - 0.5) * 0.12 - 0.04,
        r: Math.random() * 2.4 + 0.3,
        a: Math.random() * 0.2 + 0.04,
        soft: Math.random() > 0.55,
      })
    }
  }

  function draw() {
    g.clearRect(0, 0, el.width, el.height)

    for (const p of dots) {
      p.x += p.vx
      p.y += p.vy
      if (p.x < -10) p.x = el.width + 10
      if (p.x > el.width + 10) p.x = -10
      if (p.y < -10) p.y = el.height + 10
      if (p.y > el.height + 10) p.y = -10

      if (p.soft) {
        const grad = g.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r * 4)
        grad.addColorStop(0, `rgba(42, 40, 37, ${p.a * 0.5})`)
        grad.addColorStop(1, 'rgba(42, 40, 37, 0)')
        g.fillStyle = grad
        g.beginPath()
        g.arc(p.x, p.y, p.r * 4, 0, Math.PI * 2)
        g.fill()
      } else {
        g.beginPath()
        g.arc(p.x, p.y, p.r, 0, Math.PI * 2)
        g.fillStyle = `rgba(42, 40, 37, ${p.a})`
        g.fill()
      }
    }

    animationId = requestAnimationFrame(draw)
  }

  onResize = () => {
    resize()
    init()
  }

  resize()
  init()
  draw()
  window.addEventListener('resize', onResize)
}

onMounted(() => {
  if (canvasRef.value) startMist(canvasRef.value)
})

onUnmounted(() => {
  cancelAnimationFrame(animationId)
  if (onResize) window.removeEventListener('resize', onResize)
})
</script>

<template>
  <canvas ref="canvasRef" class="absolute inset-0 w-full h-full pointer-events-none opacity-80" />
</template>
