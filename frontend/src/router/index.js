/**
 * router/index.ts
 *
 * Automatic routes for `./src/pages/*.vue`
 * 
 * This project uses unplugin-vue-router for file-based routing.
 * Routes are automatically generated from the /pages folder structure:
 * 
 * pages/index.vue                    → /
 * pages/authentication/login.vue     → /authentication/login
 * pages/authentication/register.vue  → /authentication/register
 * pages/applicant/dashboard.vue      → /applicant/dashboard
 * pages/recruiter/dashboard.vue      → /recruiter/dashboard
 */

// Composables
import { createRouter, createWebHistory } from 'vue-router'
import { routes } from 'vue-router/auto-routes'
import Store from '@/states/store'
import JobDetail from '@/pages/recruiter/job-detail.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    ...routes,
    {
      path: '/recruiter/job-detail/:id',
      name: 'job-detail',
      component: JobDetail
    }
  ]
})

// Debug: Log all auto-generated routes
if (import.meta.env.DEV) {
  console.log('📍 Auto-generated routes:', routes)
}

// Navigation guard - DISABLED FOR DEVELOPMENT
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!Store.state.token
  const userRole = Store.state.user?.role

  // Debug logging
  console.log('🔍 Router Guard (DEV MODE - Auth Disabled):', {
    to: to.path,
    from: from.path,
    isAuthenticated,
    userRole,
  })
  
  // 🚧 DEVELOPMENT MODE: Allow all navigation without authentication
  console.log('✅ Navigation allowed to:', to.path, '(no auth required)')
  next()
})

// Workaround for https://github.com/vitejs/vite/issues/11804
router.onError((err, to) => {
  if (err?.message?.includes?.('Failed to fetch dynamically imported module')) {
    if (localStorage.getItem('vuetify:dynamic-reload')) {
      console.error('Dynamic import error, reloading page did not fix it', err)
    } else {
      console.log('Reloading page to fix dynamic import error')
      localStorage.setItem('vuetify:dynamic-reload', 'true')
      location.assign(to.fullPath)
    }
  } else {
    console.error(err)
  }
})

router.isReady().then(() => {
  localStorage.removeItem('vuetify:dynamic-reload')
})

export default router
