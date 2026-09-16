<script setup>
import { ref, watch } from 'vue'
import api from '@/services/axios'

const props = defineProps({
  mostrar: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['cerrar'])

const username = ref('')
const email = ref('')
const password = ref('')
const rol = ref('usuario')

function resetearFormulario() {
  username.value = ''
  email.value = ''
  password.value = ''
  rol.value = 'usuario'
}

watch(
  () => props.mostrar,
  (visible) => {
    if (visible) {
      resetearFormulario()
    }
  }
)

function cerrar() {
  emit('cerrar')
}

const crearUsuario = async () => {
    const token = localStorage.getItem('access')
    try {
        const response = await api.post('/usuarios/usuarios/', {
          username: username.value,
          email: email.value,
          password: password.value,
          rol: rol.value,
        }, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        console.log('Usuario creado exitosamente:', response.data)
        alert('Usuario creado exitosamente.')
        cerrar()
    } catch (error) {
        console.error('Error al crear usuario:', error)
        alert('Error al crear usuario. verifica los datos e inténtalo nuevamente.')
    }
}

</script>

<template>
  <div v-if="mostrar" class="modal-overlay" @click.self="cerrar">
    <section class="modal-card" role="dialog" aria-modal="true" aria-labelledby="titulo-crear-usuario">
      <header class="modal-header">
        <h2 id="titulo-crear-usuario" class="modal-titulo">Crear usuario</h2>
        <button type="button" class="modal-cerrar" aria-label="Cerrar" @click="cerrar">
          &times;
        </button>
      </header>

      <p class="modal-descripcion">
        Registra un miembro del equipo para que pueda iniciar sesión en el portal.
      </p>

      <form class="modal-form" @submit.prevent="crearUsuario">
        <section class="campo">
          <label for="nombre">Nombre de usuario <span class="obligatorio">*</span></label>
          <input id="nombre" v-model="username" type="text" placeholder="Juan Pérez" required />
        </section>

        <section class="campo">
          <label for="correo">Correo electrónico <span class="obligatorio">*</span></label>
          <input id="correo" v-model="email" type="email" placeholder="juan@empresa.com" required />
        </section>

        <section class="campo">
          <label for="contrasena">Contraseña <span class="obligatorio">*</span></label>
          <input id="contrasena" v-model="password" type="password" placeholder="••••••••" required />
        </section>

        <fieldset class="campo-rol">
          <legend>Rol asignado <span class="obligatorio">*</span></legend>

          <section class="rol-opciones">
            <label class="rol-opcion" :class="{ 'rol-opcion--activa': rol === 'usuario' }">
              <span class="rol-opcion__texto">
                <span class="rol-opcion__titulo">Usuario</span>
                <span class="rol-opcion__descripcion">Acceso a Dashboard y Tablero de notas.</span>
              </span>
              <input type="radio" value="usuario" v-model="rol" class="rol-opcion__radio" />
            </label>

            <label class="rol-opcion" :class="{ 'rol-opcion--activa': rol === 'administrador' }">
              <span class="rol-opcion__texto">
                <span class="rol-opcion__titulo">Administrador</span>
                <span class="rol-opcion__descripcion">Acceso total incluyendo administración de usuarios.</span>
              </span>
              <input type="radio" value="administrador" v-model="rol" class="rol-opcion__radio" />
            </label>
          </section>
        </fieldset>

        <footer class="modal-footer">
          <button type="button" class="btn-cancelar" @click="cerrar">Cancelar</button>
          <button type="submit" class="btn-crear">Crear usuario</button>
        </footer>
      </form>
    </section>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background-color: rgba(15, 23, 42, 0.45);
  backdrop-filter: blur(3px);
  z-index: 1000;
}

.modal-card {
  width: 100%;
  max-width: 560px;
  max-height: 90vh;
  overflow-y: auto;
  padding: 28px 32px 24px;
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 20px 50px rgba(15, 23, 42, 0.25);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

.modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}

.modal-titulo {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: #0f172a;
}

.modal-cerrar {
  padding: 2px 6px;
  font-size: 22px;
  line-height: 1;
  color: #64748b;
  background: none;
  border: none;
  cursor: pointer;
}

.modal-cerrar:hover {
  color: #0f172a;
}

.modal-descripcion {
  margin: 6px 0 22px;
  font-size: 13px;
  line-height: 1.5;
  color: #64748b;
}

.modal-form {
  display: flex;
  flex-direction: column;
}

.campo {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 16px;
}

.campo label,
.campo-rol legend {
  font-size: 13px;
  font-weight: 600;
  color: #0f172a;
}

.obligatorio {
  color: #dc2626;
}

.campo input {
  padding: 10px 14px;
  font-size: 14px;
  color: #0f172a;
  background-color: #eef1fd;
  border: 1px solid transparent;
  border-radius: 8px;
  outline: none;
  box-sizing: border-box;
}

.campo input::placeholder {
  color: #94a3b8;
}

.campo input:focus {
  border-color: #2f4fe0;
  background-color: #ffffff;
}

.campo-rol {
  margin: 4px 0 20px;
  padding: 0;
  border: none;
}

.campo-rol legend {
  margin-bottom: 10px;
  padding: 0;
}

.rol-opciones {
  display: flex;
  gap: 12px;
}

.rol-opcion {
  flex: 1;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  padding: 14px 16px;
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  cursor: pointer;
}

.rol-opcion--activa {
  border-color: #2f4fe0;
  background-color: #eef2ff;
}

.rol-opcion__texto {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.rol-opcion__titulo {
  font-size: 14px;
  font-weight: 700;
  color: #0f172a;
}

.rol-opcion__descripcion {
  font-size: 12px;
  line-height: 1.4;
  color: #64748b;
}

.rol-opcion__radio {
  width: 18px;
  height: 18px;
  margin-top: 2px;
  accent-color: #2f4fe0;
  cursor: pointer;
  flex-shrink: 0;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 8px;
}

.btn-cancelar {
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 600;
  color: #0f172a;
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  cursor: pointer;
}

.btn-cancelar:hover {
  background-color: #f8fafc;
}

.btn-crear {
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 600;
  color: #ffffff;
  background-color: #2f4fe0;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.btn-crear:hover {
  background-color: #2440c2;
}
</style>