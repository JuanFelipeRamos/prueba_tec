<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import NavbarComponent from '@/components/NavbarComponent.vue'
import { obtenerPerfilUsuario } from '@/services/obtenerPerfilUsuario'
import ModalCrearUsuarios from '@/components/ModalCrearUsuarios.vue'
import ModalActivarDesactivarUsuarios from '@/components/ModalActivarDesactivarUsuarios.vue'
import ModalBorrarUsuarios from '@/components/ModalBorrarUsuarios.vue'
import ModalEditarUsuarios from '@/components/ModalEditarUsuarios.vue'
import api from '@/services/axios'

const token = ref(localStorage.getItem('access'))
const router = useRouter()
const userRole = ref('')
const listaUsuarios = ref([])

// listar todos los usuarios
const listarUsuarios = async () => {
    try {
        const response = await api.get('/usuarios/usuarios/', {
            headers: {
                'Authorization': `Bearer ${token.value}`
            }
        })
        listaUsuarios.value = response.data
        console.log('Usuarios obtenidos:', listaUsuarios.value)

        if (listaUsuarios.value.length === 0) {
            alert('No se encontraron usuarios en el sistema.')
        }
    } catch (error) {
        console.error('Error al listar usuarios:', error)
        alert('Error al listar usuarios. Inténtalo nuevamente.')
    }
}

const totalUsuarios = computed(() => listaUsuarios.value.length)
const totalActivos = computed(() => listaUsuarios.value.filter((u) => u.is_active === true).length)
const totalInactivos = computed(() => listaUsuarios.value.filter((u) => u.is_active === false).length)
const totalAdmins = computed(() => listaUsuarios.value.filter((u) => u.rol === 'administrador').length)

function estadoATexto(is_active) {
  const estado = ref("")

  if (is_active == true) {
    estado.value = "Activo"
  } else {
    estado.value = "Inactivo"
  }

  return estado.value
}

// obtener el perfil del usuario autenticado y redirigir si no es administrador
const obtenerPerfil = async () => {
  const ususarioAutenticado = await obtenerPerfilUsuario()
  userRole.value = ususarioAutenticado.rol;

  if (userRole.value !== 'administrador' && token.value) {
      router.push('/tablero')
  }
}

onMounted(() => {
    listarUsuarios()
    obtenerPerfil()
  if (!token.value) {
    alert('No se encontró token de acceso. Redirigiendo a la página de inicio de sesión.')
    router.push('/')
  }
})

const mostrarModalCrear = ref(false)

function crearUsuario() {
  mostrarModalCrear.value = true
}

function cerrarModalCrear() {
  mostrarModalCrear.value = false
}

// confirmación para activar/desactivar un usuario
const mostrarModalEstado = ref(false)
const usuarioSeleccionado = ref(null)
const accionSeleccionada = ref('desactivar')

function abrirModalEstado(usuario, accion) {
  usuarioSeleccionado.value = usuario
  accionSeleccionada.value = accion
  mostrarModalEstado.value = true
}

function cerrarModalEstado() {
  mostrarModalEstado.value = false
  usuarioSeleccionado.value = null
}

// confirmar el cambio de estado del usuario
async function confirmarCambioEstado(usuario) {
  const nuevoEstado = accionSeleccionada.value === 'activar'

  try {
    await api.patch(
      `/usuarios/usuarios/${usuario.id}/`,
      { is_active: nuevoEstado },
      {
        headers: {
          Authorization: `Bearer ${token.value}`,
        },
      }
    )

    const usuarioEnLista = listaUsuarios.value.find((u) => u.id === usuario.id)
    if (usuarioEnLista) {
      usuarioEnLista.is_active = nuevoEstado
    }
  } catch (error) {
    console.error('Error al cambiar el estado del usuario:', error)
    alert('Error al cambiar el estado del usuario.')
  } finally {
    cerrarModalEstado()
  }
}

// borrar usuario
const mostrarModalBorrar = ref(false)
const usuarioABorrar = ref(null)

function abrirModalBorrar(usuario) {
  usuarioABorrar.value = usuario
  mostrarModalBorrar.value = true
}

function cerrarModalBorrar() {
  mostrarModalBorrar.value = false
  usuarioABorrar.value = null
}

// editar usuario
const mostrarModalEditar = ref(false)
const usuarioAEditar = ref(null)

function abrirModalEditar(usuario) {
  usuarioAEditar.value = usuario
  mostrarModalEditar.value = true
}

function cerrarModalEditar() {
  mostrarModalEditar.value = false
  usuarioAEditar.value = null
}

function onUsuarioEditado(cambios) {
  const usuarioEnLista = listaUsuarios.value.find((u) => u.id === cambios.id)
  if (usuarioEnLista) {
    if (cambios.username !== undefined) usuarioEnLista.username = cambios.username
    if (cambios.email !== undefined) usuarioEnLista.email = cambios.email
    if (cambios.rol !== undefined) usuarioEnLista.rol = cambios.rol
  }
}
</script>

<template>
  <main class="usuarios-page">
    <NavbarComponent />
    <header class="usuarios-header">
      <h1 class="usuarios-title">Administración de usuarios</h1>
      <button type="button" class="btn-crear-usuario" @click="crearUsuario">
        Crear usuario
      </button>
    </header>

    <section class="regla-seguridad">
      <h2 class="regla-titulo">Regla del sistema de seguridad</h2>
      <p class="regla-texto">
        Siempre debe existir al menos un administrador activo en el sistema. Los usuarios inactivos no pueden iniciar sesión.
      </p>
    </section>

    <section class="tabla-contenedor">
      <header class="tabla-resumen">
        <span class="resumen-total">Todos los usuarios ({{ totalUsuarios }})</span>
        <span class="resumen-activos">{{ totalActivos }} Activos</span>
        <span class="separador">•</span>
        <span class="resumen-inactivos">{{ totalInactivos }} Inactivo{{ totalInactivos === 1 ? '' : 's' }}</span>
      </header>

      <table class="usuarios-tabla">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Correo electrónico</th>
            <th>Rol</th>
            <th>Estado</th>
            <th class="col-acciones">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="usuario in listaUsuarios" :key="usuario.id">
            <td>
              <span class="usuario-nombre">{{ usuario.username }}</span>
            </td>
            <td class="usuario-correo">{{ usuario.email }}</td>
            <td>
              <span class="badge-rol" :class="usuario.rol === 'Administrador' ? 'badge-rol--admin' : 'badge-rol--usuario'">
                {{ usuario.rol }}
              </span>
            </td>
            <td>
              <span class="badge-estado" :class="usuario.is_active === true ? 'badge-estado--activo' : 'badge-estado--inactivo'">
                {{ estadoATexto(usuario.is_active) }}
              </span>
            </td>
            <td class="col-acciones">
              <section class="acciones">
                <button type="button" class="btn-borrar" @click="abrirModalBorrar(usuario)">
                  Borrar
                </button>
                <button type="button" class="btn-editar" @click="abrirModalEditar(usuario)">
                  Editar
                </button>
                <button
                  v-if="usuario.is_active"
                  type="button"
                  class="btn-desactivar"
                  :disabled="usuario.esUsuarioActual"
                  @click="abrirModalEstado(usuario, 'desactivar')"
                >
                  Desactivar
                </button>
                <button v-else type="button" class="btn-activar" @click="abrirModalEstado(usuario, 'activar')">
                  Activar
                </button>
              </section>
            </td>
          </tr>
        </tbody>
      </table>
    </section>

    <section class="usuarios-stats">
      <article class="stat-card">
        <span class="stat-label">Total miembros</span>
        <span class="stat-valor">{{ totalUsuarios }}</span>
      </article>
      <article class="stat-card">
        <span class="stat-label">Admins designados</span>
        <span class="stat-valor">{{ totalAdmins }}</span>
      </article>
    </section>

    <ModalCrearUsuarios
      :mostrar="mostrarModalCrear"
      @cerrar="cerrarModalCrear"
    />

    <ModalActivarDesactivarUsuarios
      :mostrar="mostrarModalEstado"
      :usuario="usuarioSeleccionado"
      :accion="accionSeleccionada"
      @cerrar="cerrarModalEstado"
      @confirmar="confirmarCambioEstado"
    />

    <ModalBorrarUsuarios
      :mostrar="mostrarModalBorrar"
      :usuario="usuarioABorrar"
      @cerrar="cerrarModalBorrar"
    />

    <ModalEditarUsuarios
      :mostrar="mostrarModalEditar"
      :usuario="usuarioAEditar"
      @cerrar="cerrarModalEditar"
      @editado="onUsuarioEditado"
    />
  </main>
</template>

<style scoped>
.usuarios-page {
  min-height: 100%;
  background-color: #f5f6fd;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

.usuarios-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 28px 32px 20px;
}

.usuarios-title {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #0f172a;
}

.btn-crear-usuario {
  padding: 10px 18px;
  font-size: 14px;
  font-weight: 600;
  color: #ffffff;
  background-color: #2f4fe0;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.btn-crear-usuario:hover {
  background-color: #2440c2;
}

.regla-seguridad {
  margin: 0 32px 20px;
  padding: 16px 20px;
  background-color: #e2e9fb;
  border-radius: 10px;
}

.regla-titulo {
  margin: 0 0 4px 0;
  font-size: 14px;
  font-weight: 700;
  color: #0f172a;
}

.regla-texto {
  margin: 0;
  font-size: 13px;
  color: #475569;
}

.tabla-contenedor {
  margin: 0 32px 20px;
  background-color: #ffffff;
  border: 1px solid #eef0f7;
  border-radius: 12px;
  overflow: hidden;
}

.tabla-resumen {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 20px;
  font-size: 13px;
  color: #64748b;
  background-color: #f2f4fc;
  border-bottom: 1px solid #eef0f7;
}

.resumen-total {
  font-weight: 700;
  color: #0f172a;
}

.resumen-activos {
  color: #1d4ed8;
}

.resumen-inactivos {
  color: #b45309;
}

.usuarios-tabla {
  width: 100%;
  border-collapse: collapse;
}

.usuarios-tabla th {
  padding: 14px 20px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  text-align: left;
  color: #64748b;
  border-bottom: 1px solid #eef0f7;
}

.usuarios-tabla td {
  padding: 16px 20px;
  font-size: 14px;
  color: #0f172a;
  border-bottom: 1px solid #f1f2f9;
  vertical-align: middle;
}

.usuarios-tabla tbody tr:last-child td {
  border-bottom: none;
}

.usuario-nombre {
  display: block;
  font-weight: 600;
}

.usuario-actual {
  display: block;
  font-size: 12px;
  font-weight: 400;
  color: #94a3b8;
}

.usuario-correo {
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  color: #475569;
}

.badge-rol,
.badge-estado {
  display: inline-block;
  padding: 4px 12px;
  font-size: 12px;
  font-weight: 600;
  border-radius: 999px;
}

.badge-rol--admin,
.badge-rol--usuario {
  color: #3730a3;
  background-color: #e0e4fb;
}

.badge-estado--activo {
  color: #1e3a8a;
  background-color: #dbe5fb;
}

.badge-estado--inactivo {
  color: #92400e;
  background-color: #fde3c0;
}

.col-acciones {
  width: 1%;
  white-space: nowrap;
  text-align: right;
}

.acciones {
  display: inline-flex;
  align-items: center;
  gap: 10px;
}

.btn-editar {
  padding: 6px 14px;
  font-size: 13px;
  font-weight: 600;
  color: #1d4ed8;
  background-color: #e2e9fb;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.btn-editar:hover {
  background-color: #d3dcf8;
}

.btn-borrar {
  padding: 6px 14px;
  font-size: 13px;
  font-weight: 600;
  color: #dc2626;
  background-color: #e2e9fb;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.btn-borrar:hover {
  background-color: #d3dcf8;
}

.btn-desactivar {
  padding: 6px 4px;
  font-size: 13px;
  font-weight: 600;
  color: #dc2626;
  background: none;
  border: none;
  cursor: pointer;
}

.btn-desactivar:hover:not(:disabled) {
  text-decoration: underline;
}

.btn-desactivar:disabled {
  color: #cbd5e1;
  cursor: not-allowed;
}

.btn-activar {
  padding: 6px 14px;
  font-size: 13px;
  font-weight: 600;
  color: #ffffff;
  background-color: #2f4fe0;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.btn-activar:hover {
  background-color: #2440c2;
}

.usuarios-stats {
  display: flex;
  gap: 20px;
  margin: 0 32px 32px;
}

.stat-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 18px 20px;
  background-color: #e2e9fb;
  border-radius: 10px;
}

.stat-label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: #475569;
}

.stat-valor {
  font-size: 26px;
  font-weight: 700;
  color: #1d3fd6;
}
</style>