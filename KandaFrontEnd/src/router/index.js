import { createRouter, createWebHistory } from 'vue-router'
import tokenManager from '../utils/tokenManager'

// Importar vistas de autenticación
import LoginView from '../views/authviews/LoginView.vue'
import RegisterView from '../views/authviews/RegisterView.vue'
import DashboardView from '../views/authviews/DashboardView.vue'
import ActivationView from '../views/authviews/ActivationView.vue'
import ActivationInvalidView from '../views/authviews/ActivationInvalidView.vue'
import ActivationEmailView from '../views/authviews/ActivationEmailView.vue'
import ResendActivationView from '../views/authviews/ResendActivationView.vue'

// Guard de autenticación para rutas protegidas
const requireAuth = (to, from, next) => {
  if (!tokenManager.isAuthenticated()) {
    // Redirigir a login si no está autenticado
    next({ name: 'login' })
  } else {
    next()
  }
}

// Guard para rutas de invitados (login, registro, etc.)
const requireGuest = (to, from, next) => {
  if (tokenManager.isAuthenticated()) {
    // Redirigir al dashboard si ya está autenticado
    next({ name: 'dashboard' })
  } else {
    next()
  }
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // Ruta principal redirige a dashboard o login según autenticación
    {
      path: '/',
      redirect: to => {
        return tokenManager.isAuthenticated() ? { name: 'dashboard' } : { name: 'login' }
      }
    },
    
    // Rutas de autenticación (accesibles solo para invitados)
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      beforeEnter: requireGuest
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      beforeEnter: requireGuest
    },
    {
      path: '/activate-email',
      name: 'activate-email',
      component: ActivationEmailView,
      beforeEnter: requireGuest
    },
    {
      path: '/activate-invalid',
      name: 'activate-invalid',
      component: ActivationInvalidView,
      beforeEnter: requireGuest
    },
    {
      path: '/activate/:uidb64/:token',
      name: 'activate',
      component: ActivationView,
      props: true,
      beforeEnter: requireGuest
    },
    {
      path: '/resend-activation',
      name: 'resend-activation',
      component: ResendActivationView,
      beforeEnter: requireGuest
    },
    
    // Rutas protegidas (requieren autenticación)
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      beforeEnter: requireAuth
    },
    
    // Ruta para 404 - No encontrado
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue')
    }
  ],
})

export default router
