<script setup lang="ts">
/**
 * 水墨山水：远近层峦 + 云雾缓移
 */
</script>

<template>
  <div class="ink-landscape absolute inset-0 overflow-hidden pointer-events-none" aria-hidden="true">
    <!-- 宣纸底色 -->
    <div class="absolute inset-0 ink-sky" />

    <!-- 远山 -->
    <svg
      class="absolute bottom-[18%] left-0 w-[120%] h-[42%] opacity-[0.18] ink-layer ink-far"
      viewBox="0 0 1440 320"
      preserveAspectRatio="none"
    >
      <path
        fill="#3a3a38"
        d="M0,220 C120,180 220,140 340,155 C460,170 520,210 640,190 C780,165 860,100 980,120 C1100,140 1180,180 1280,160 C1360,145 1410,130 1440,125 L1440,320 L0,320 Z"
      />
    </svg>

    <!-- 中景山 -->
    <svg
      class="absolute bottom-[8%] left-[-5%] w-[110%] h-[48%] opacity-[0.28] ink-layer ink-mid"
      viewBox="0 0 1440 360"
      preserveAspectRatio="none"
    >
      <path
        fill="#2a2825"
        d="M0,260 C80,220 160,160 280,175 C400,190 450,240 560,220 C680,195 740,120 860,140 C980,160 1040,210 1160,185 C1260,165 1340,140 1440,150 L1440,360 L0,360 Z"
      />
      <path
        fill="#2a2825"
        opacity="0.55"
        d="M200,280 C300,230 380,200 480,215 C580,230 620,270 720,250 C840,225 900,170 1020,190 C1120,205 1200,240 1320,220 L1320,360 L200,360 Z"
      />
    </svg>

    <!-- 近景山崖 -->
    <svg
      class="absolute bottom-0 right-0 w-[72%] md:w-[58%] h-[58%] opacity-[0.38] ink-layer ink-near"
      viewBox="0 0 800 520"
      preserveAspectRatio="xMaxYMax meet"
    >
      <path
        fill="#1f1e1c"
        d="M320,520 L360,380 C380,320 420,280 480,260 C520,245 560,200 600,180 C640,160 680,140 720,100 C750,70 780,40 800,20 L800,520 Z"
      />
      <path
        fill="#1f1e1c"
        opacity="0.7"
        d="M180,520 L220,420 C250,360 290,330 340,320 C390,310 430,280 470,250 C510,220 560,200 620,190 L620,520 Z"
      />
      <!-- 松意疏笔 -->
      <g opacity="0.45" stroke="#1f1e1c" stroke-width="1.2" fill="none">
        <path d="M520,250 C525,230 518,210 530,190" />
        <path d="M530,210 C515,205 540,200 525,195" />
        <path d="M528,200 C512,198 542,192 520,188" />
      </g>
    </svg>

    <!-- 近景左岸 -->
    <svg
      class="absolute bottom-0 left-0 w-[45%] h-[28%] opacity-[0.22] ink-layer ink-shore"
      viewBox="0 0 600 200"
      preserveAspectRatio="none"
    >
      <path
        fill="#2a2825"
        d="M0,120 C80,90 140,100 200,85 C280,65 340,90 400,100 C480,115 540,95 600,110 L600,200 L0,200 Z"
      />
    </svg>

    <!-- 云雾层 -->
    <div class="mist mist-a" />
    <div class="mist mist-b" />
    <div class="mist mist-c" />

    <!-- 水墨晕染斑 -->
    <div class="absolute top-[12%] right-[18%] w-48 h-48 rounded-full ink-blot ink-blot-a" />
    <div class="absolute top-[35%] right-[40%] w-32 h-32 rounded-full ink-blot ink-blot-b" />
    <div class="absolute bottom-[30%] left-[12%] w-40 h-24 ink-blot ink-blot-c" />
    <div class="absolute top-[55%] left-[35%] w-24 h-24 rounded-full ink-blot ink-blot-d" />
  </div>
</template>

<style scoped>
.ink-sky {
  background:
    radial-gradient(ellipse 80% 50% at 70% 30%, rgba(90, 100, 95, 0.12), transparent 60%),
    radial-gradient(ellipse 60% 40% at 20% 60%, rgba(42, 40, 37, 0.06), transparent 50%),
    linear-gradient(165deg, #ebe8e2 0%, #e2dfd7 38%, #d5d2c8 72%, #c9c6bc 100%);
}

.ink-layer {
  filter: blur(0.3px);
}

.ink-far {
  animation: mountain-breathe 14s ease-in-out infinite;
}

.ink-mid {
  animation: mountain-breathe 11s ease-in-out infinite 1s;
}

.ink-near {
  animation: mountain-rise 1.4s ease-out both;
}

.ink-shore {
  animation: mountain-rise-shore 1.6s ease-out 0.2s both;
}

.mist {
  position: absolute;
  height: 34%;
  width: 160%;
  left: -30%;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(245, 243, 238, 0.8) 18%,
    rgba(232, 229, 222, 0.98) 50%,
    rgba(245, 243, 238, 0.75) 82%,
    transparent 100%
  );
  filter: blur(20px);
  pointer-events: none;
}

.mist-a {
  bottom: 24%;
  animation: mist-drift 20s linear infinite;
  opacity: 1;
}

.mist-b {
  bottom: 38%;
  height: 24%;
  animation: mist-drift 28s linear infinite reverse;
  opacity: 0.88;
}

.mist-c {
  bottom: 8%;
  height: 28%;
  animation: mist-drift 24s linear infinite;
  opacity: 0.92;
  animation-delay: -5s;
}

.ink-blot {
  background: radial-gradient(circle, rgba(42, 40, 37, 0.2) 0%, transparent 70%);
  filter: blur(22px);
  pointer-events: none;
}

.ink-blot-a {
  opacity: 0.12;
  animation: blot-float 14s ease-in-out infinite;
}

.ink-blot-b {
  opacity: 0.09;
  animation: blot-float 11s ease-in-out infinite reverse;
  animation-delay: -2s;
}

.ink-blot-c {
  opacity: 0.1;
  border-radius: 60% 40% 55% 45%;
  background: radial-gradient(ellipse, rgba(62, 79, 92, 0.18) 0%, transparent 70%);
  animation: blot-float 18s ease-in-out infinite;
  animation-delay: -5s;
}

.ink-blot-d {
  opacity: 0.08;
  animation: blot-float 9s ease-in-out infinite;
  animation-delay: -1s;
}

@keyframes blot-float {
  0%,
  100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(12px, -10px) scale(1.06);
  }
  66% {
    transform: translate(-8px, 6px) scale(0.96);
  }
}

@keyframes mist-drift {
  0% {
    transform: translateX(-16%);
  }
  100% {
    transform: translateX(16%);
  }
}

@keyframes mountain-breathe {
  0%,
  100% {
    opacity: 0.16;
    transform: translateY(0);
  }
  50% {
    opacity: 0.22;
    transform: translateY(-4px);
  }
}

@keyframes mountain-rise {
  from {
    opacity: 0;
    transform: translateY(24px);
  }
  to {
    opacity: 0.38;
    transform: translateY(0);
  }
}

@keyframes mountain-rise-shore {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 0.22;
    transform: translateY(0);
  }
}

@media (prefers-reduced-motion: reduce) {
  .mist-a,
  .mist-b,
  .mist-c,
  .ink-far,
  .ink-mid,
  .ink-near,
  .ink-shore,
  .ink-blot-a,
  .ink-blot-b,
  .ink-blot-c,
  .ink-blot-d {
    animation: none;
  }
}
</style>
