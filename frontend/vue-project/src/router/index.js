import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import NavbarComponent from '../components/NavbarComponent.vue'
import TableroView from '../views/TableroView.vue'
import NotaCardComponent from '@/components/NotaCardComponent.vue'
import GestionUsuariosView from '@/views/GestionUsuariosView.vue'
import ModalCrearUsuarios from '@/components/ModalCrearUsuarios.vue'
import ModalActivarDesactivarUsuarios from '@/components/ModalActivarDesactivarUsuarios.vue'
import ModalBorrarUsuarios from '@/components/ModalBorrarUsuarios.vue'
import ModalEditarUsuarios from '@/components/ModalEditarUsuarios.vue'

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
    },

    {
      path: '/nota/:id',
      name: 'NotaCard',
      component: NotaCardComponent,
    },

    {
      path: '/gestion-usuarios',
      name: 'GestionUsuarios',
      component: GestionUsuariosView,
    },

    {
      path: '/modal-crear-usuarios',
      name: 'ModalCrearUsuarios',
      component: ModalCrearUsuarios,
    },

    {
      path: '/modal-crear-usuarios',
      name: 'ModalCrearUsuarios',
      component: ModalCrearUsuarios,
    },

    {
      path: '/modal-activar-desactivar-usuarios',
      name: 'ModalActivarDesactivarUsuarios',
      component: ModalActivarDesactivarUsuarios,
    },

    {
      path: '/modal-borrar-usuarios',
      name: 'ModalBorrarUsuarios',
      component: ModalBorrarUsuarios,
    },

    {
      path: '/modal-editar-usuarios',
      name: 'ModalEditarUsuarios',
      component: ModalEditarUsuarios,
    },
  ],
})

export default router
