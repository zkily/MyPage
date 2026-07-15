import { createRouter, createWebHistory } from 'vue-router'
import { getAuthToken } from '@/api'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('@/views/SiteLayout.vue'),
      children: [
        {
          path: '',
          name: 'home',
          component: () => import('@/views/HomeView.vue'),
        },
        {
          path: 'about',
          name: 'about',
          component: () => import('@/views/AboutView.vue'),
        },
        {
          path: 'projects',
          name: 'projects',
          component: () => import('@/views/ProjectsView.vue'),
        },
        {
          path: 'records',
          name: 'records',
          component: () => import('@/views/RecordsView.vue'),
        },
        {
          path: 'knowledge',
          name: 'knowledge',
          component: () => import('@/views/KnowledgeView.vue'),
        },
        {
          path: 'contact',
          name: 'contact',
          component: () => import('@/views/ContactView.vue'),
        },
      ],
    },
    {
      path: '/admin/login',
      name: 'admin-login',
      component: () => import('@/views/admin/LoginView.vue'),
      meta: { guest: true },
    },
    {
      path: '/admin',
      component: () => import('@/views/admin/AdminLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'admin-dashboard',
          component: () => import('@/views/admin/DashboardView.vue'),
        },
        {
          path: 'projects',
          name: 'admin-projects',
          component: () => import('@/views/admin/ProjectsListView.vue'),
        },
        {
          path: 'projects/new',
          name: 'admin-project-new',
          component: () => import('@/views/admin/ProjectEditor.vue'),
        },
        {
          path: 'projects/:id',
          name: 'admin-project-edit',
          component: () => import('@/views/admin/ProjectEditor.vue'),
        },
        {
          path: 'knowledge',
          name: 'admin-knowledge',
          component: () => import('@/views/admin/KnowledgeListView.vue'),
        },
        {
          path: 'knowledge/new',
          name: 'admin-knowledge-new',
          component: () => import('@/views/admin/KnowledgeEditor.vue'),
        },
        {
          path: 'knowledge/:id',
          name: 'admin-knowledge-edit',
          component: () => import('@/views/admin/KnowledgeEditor.vue'),
        },
      ],
    },
  ],
  scrollBehavior() {
    return { top: 0 }
  },
})

router.beforeEach((to) => {
  const token = getAuthToken()
  if (to.meta.requiresAuth && !token) {
    return { name: 'admin-login' }
  }
  if (to.meta.guest && token) {
    return { name: 'admin-dashboard' }
  }
})

export default router
