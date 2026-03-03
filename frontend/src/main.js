import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import DashboardView from './views/dashboard.vue'
import LoginView from './views/Login.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/',          redirect: '/login' },
    { path: '/login',     component: LoginView },
    { path: '/patient',   component: DashboardView },
    { path: '/dashboard', redirect: '/patient' },
  ]
})

// ─── Navigation Guard ──────────────────────────────────────────────────────
// Redirects to /login if trying to access protected routes without a session
router.beforeEach((to) => {
  const isLoggedIn = localStorage.getItem('isLoggedIn')
  if (to.path !== '/login' && !isLoggedIn) {
    return '/login'
  }
  return true
})

createApp(App).use(router).mount('#app')
