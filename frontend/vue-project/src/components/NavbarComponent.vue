<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router';
import { obtenerPerfilUsuario } from '@/services/obtenerPerfilUsuario'

const userName = ref('')
const userRole = ref('')
const router = useRouter()
const linkGestionarUsuarios = ref(true)

function cerrarSesion() {
  localStorage.removeItem('access')
  router.push('/')
  console.log('Sesión cerrada.')
}

const obtenerPerfil = async () => {
  const ususarioAutenticado = await obtenerPerfilUsuario()
  userName.value = ususarioAutenticado.username;
  userRole.value = ususarioAutenticado.rol;

  if (userRole.value !== 'administrador') {
      linkGestionarUsuarios.value = false;
  }
}

onMounted(() => {
  obtenerPerfil()
})

</script>

<template>
  <header class="navbar">
    <nav class="navbar-left">
      <span class="brand">PORTAL DEL EQUIPO</span>

      <ul class="nav-links">
        <li>
          <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
        </li>
        <li>
          <router-link to="/tablero" class="nav-link">Tablero de notas</router-link>
        </li>
        <li class="nav-link-with-badge" v-if="linkGestionarUsuarios">
          <router-link to="/gestion-usuarios" class="nav-link">Usuarios</router-link>
        </li>
      </ul>
    </nav>

    <section class="navbar-right">
      <section class="user-info">
        <span class="user-name">{{ userName }}</span>
        <span class="user-role">{{ userRole }}</span>
      </section>

      <a href="#" class="logout-link" @click.prevent="cerrarSesion">Cerrar sesión</a>
    </section>
  </header>
</template>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 14px 24px;
  background-color: #f5f6fd;
  border-bottom: 1px solid #e5e7eb;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  box-sizing: border-box;
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: 32px;
}

.brand {
  font-size: 16px;
  font-weight: 700;
  color: #0f172a;
  white-space: nowrap;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 8px;
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-link {
  display: inline-block;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 500;
  color: #4b5563;
  text-decoration: none;
  border-radius: 8px;
  white-space: nowrap;
  transition: background-color 0.15s ease, color 0.15s ease;
}

.nav-link:hover {
  background-color: #3b5bfd;
  color: #ffffff;
}

.nav-link-with-badge {
  display: flex;
  align-items: center;
  gap: 6px;
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  line-height: 1.3;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: #0f172a;
}

.user-role {
  font-size: 12px;
  color: #6b7280;
}

.logout-link {
  font-size: 14px;
  font-weight: 500;
  color: #dc2626;
  text-decoration: none;
  white-space: nowrap;
}

.logout-link:hover {
  text-decoration: underline;
}
</style>