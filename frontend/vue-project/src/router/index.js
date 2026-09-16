import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import NavbarComponent from '../components/NavbarComponent.vue'
import TableroView from '../views/TableroView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Login',
      component: LoginView,
    },

    {
      path: '/navbar',
      name: 'Navbar',
      component: NavbarComponent,
    },

    {
      path: '/tablero',
      name: 'Tablero',
      component: TableroView,
    }
  ],
})

export default router
