<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'

/** 全站淡墨山水背景：远山呼吸 + 云雾 + 墨点漂浮 */
const canvasRef = ref<HTMLCanvasElement | null>(null)

let animationId = 0
let onResize: (() => void) | null = null

type InkDot = {
  x: number
  y: number
  vx: number
  vy: number
  r: number
  a: number
  pulse: number
  soft: boolean
}

function startInk(el: HTMLCanvasElement) {
  const ctx = el.getContext('2d')
  if (!ctx) return
  const g = ctx

  const dots: InkDot[] = []
  const count = 42

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
        vx: (Math.random() - 0.35) * 0.16,
        vy: (Math.random() - 0.5) * 0.1 - 0.03,
        r: Math.random() * 3 + 0.5,
        a: Math.random() * 0.18 + 0.04,
        pulse: Math.random() * Math.PI * 2,
        soft: Math.random() > 0.4,
      })
    }
  }

  function draw() {
    g.clearRect(0, 0, el.width, el.height)

    for (const p of dots) {
      p.x += p.vx
      p.y += p.vy
      p.pulse += 0.008
      if (p.x < -20) p.x = el.width + 20
      if (p.x > el.width + 20) p.x = -20
      if (p.y < -20) p.y = el.height + 20
      if (p.y > el.height + 20) p.y = -20

      const breathe = 0.7 + Math.sin(p.pulse) * 0.3
      const alpha = p.a * breathe

      if (p.soft) {
        const rad = p.r * (3.5 + Math.sin(p.pulse) * 0.8)
        const grad = g.createRadialGradient(p.x, p.y, 0, p.x, p.y, rad)
        grad.addColorStop(0, `rgba(42, 40, 37, ${alpha * 0.55})`)
        grad.addColorStop(0.55, `rgba(62, 79, 92, ${alpha * 0.18})`)
        grad.addColorStop(1, 'rgba(42, 40, 37, 0)')
        g.fillStyle = grad
        g.beginPath()
        g.arc(p.x, p.y, rad, 0, Math.PI * 2)
        g.fill()
      } else {
        g.beginPath()
        g.arc(p.x, p.y, p.r * breathe, 0, Math.PI * 2)
        g.fillStyle = `rgba(42, 40, 37, ${alpha})`
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
  if (canvasRef.value) startInk(canvasRef.value)
})

onUnmounted(() => {
  cancelAnimationFrame(animationId)
  if (onResize) window.removeEventListener('resize', onResize)
})
</script>

<template>
  <div class="site-ink-bg" aria-hidden="true">
    <!-- 远山剪影 -->
    <svg
      class="site-ink-mountains site-ink-far"
      viewBox="0 0 1440 280"
      preserveAspectRatio="none"
    >
      <path
        fill="#2a2825"
        d="M0,200 C160,150 280,120 420,140 C560,160 640,200 780,170 C920,140 1040,90 1180,110 C1280,125 1360,150 1440,140 L1440,280 L0,280 Z"
      />
    </svg>
    <svg
      class="site-ink-mountains site-ink-mid"
      viewBox="0 0 1440 240"
      preserveAspectRatio="none"
    >
      <path
        fill="#1f1e1c"
        d="M0,180 C120,140 240,100 380,120 C520,140 600,180 740,155 C880,130 980,80 1120,100 C1240,115 1340,140 1440,130 L1440,240 L0,240 Z"
      />
    </svg>

    <!-- 云雾带 -->
    <div class="site-mist site-mist-a" />
    <div class="site-mist site-mist-b" />
    <div class="site-mist site-mist-c" />

    <!-- 墨晕斑 -->
    <div class="site-blot site-blot-1" />
    <div class="site-blot site-blot-2" />
    <div class="site-blot site-blot-3" />

    <canvas ref="canvasRef" class="site-ink-canvas" />
  </div>
</template>

<style scoped>
.site-ink-bg {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.site-ink-mountains {
  position: absolute;
  left: -5%;
  width: 110%;
  bottom: 0;
  height: min(38vh, 320px);
}

.site-ink-far {
  opacity: 0.06;
  animation: ink-breathe 16s ease-in-out infinite;
}

.site-ink-mid {
  opacity: 0.09;
  height: min(28vh, 240px);
  animation: ink-breathe 12s ease-in-out infinite 1.5s;
}

.site-mist {
  position: absolute;
  width: 170%;
  left: -35%;
  height: 30%;
  filter: blur(26px);
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(245, 243, 238, 0.8) 20%,
    rgba(230, 228, 222, 0.98) 48%,
    rgba(245, 243, 238, 0.75) 75%,
    transparent 100%
  );
}

.site-mist-a {
  bottom: 14%;
  opacity: 0.95;
  animation: mist-drift 24s linear infinite;
}

.site-mist-b {
  bottom: 28%;
  height: 22%;
  opacity: 0.8;
  animation: mist-drift 32s linear infinite reverse;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(215, 213, 206, 0.75) 22%,
    rgba(235, 233, 227, 0.95) 50%,
    rgba(215, 213, 206, 0.7) 78%,
    transparent 100%
  );
}

.site-mist-c {
  top: 8%;
  height: 26%;
  opacity: 0.7;
  animation: mist-drift 28s linear infinite;
  animation-delay: -8s;
}

.site-blot {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(42, 40, 37, 0.14) 0%, transparent 70%);
  filter: blur(24px);
  animation: blot-pulse 10s ease-in-out infinite;
}

.site-blot-1 {
  width: 18rem;
  height: 18rem;
  top: 8%;
  right: 6%;
  opacity: 0.7;
}

.site-blot-2 {
  width: 14rem;
  height: 14rem;
  top: 42%;
  left: 4%;
  opacity: 0.5;
  animation-delay: -3s;
  background: radial-gradient(circle, rgba(62, 79, 92, 0.12) 0%, transparent 70%);
}

.site-blot-3 {
  width: 22rem;
  height: 12rem;
  bottom: 22%;
  right: 28%;
  opacity: 0.4;
  animation-delay: -6s;
  border-radius: 60% 40% 50% 50%;
}

.site-ink-canvas {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  opacity: 0.85;
}

@keyframes mist-drift {
  0% {
    transform: translateX(-14%);
  }
  100% {
    transform: translateX(14%);
  }
}

@keyframes ink-breathe {
  0%,
  100% {
    transform: translateY(0);
    opacity: 0.06;
  }
  50% {
    transform: translateY(-6px);
    opacity: 0.1;
  }
}

.site-ink-mid {
  animation-name: ink-breathe-mid;
}

@keyframes ink-breathe-mid {
  0%,
  100% {
    transform: translateY(0);
    opacity: 0.08;
  }
  50% {
    transform: translateY(-4px);
    opacity: 0.12;
  }
}

@keyframes blot-pulse {
  0%,
  100% {
    transform: scale(1);
    opacity: 0.45;
  }
  50% {
    transform: scale(1.08);
    opacity: 0.7;
  }
}

@media (prefers-reduced-motion: reduce) {
  .site-ink-far,
  .site-ink-mid,
  .site-mist-a,
  .site-mist-b,
  .site-mist-c,
  .site-blot {
    animation: none;
  }
}
</style>
