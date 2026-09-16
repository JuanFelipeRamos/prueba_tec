<script setup>
import api from '@/services/axios'

const props = defineProps({
  mostrar: {
    type: Boolean,
    default: false,
  },
  usuario: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['cerrar'])

function cerrar() {
  emit('cerrar')
}

const borrarUsuario = async () => {
  const token = localStorage.getItem('access')
  try {
    await api.delete(`/usuarios/usuarios/${props.usuario.id}/`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    console.log('Usuario borrado exitosamente.')
    alert('Usuario borrado exitosamente.')
    cerrar()
  } catch (error) {
    console.error('Error al borrar usuario:', error)
    alert('Error al borrar usuario. Inténtalo nuevamente.')
  }
}
</script>

<template>
  <div v-if="mostrar" class="modal-overlay" @click.self="cerrar">
    <section class="modal-card" role="dialog" aria-modal="true" aria-labelledby="titulo-confirmar-estado">
      <header class="modal-header">
        <h2 id="titulo-confirmar-estado" class="modal-titulo">¿Deseas borrar al usuario <strong>{{ usuario?.username }}</strong>?</h2>
      </header>

      <footer class="modal-footer">
        <button type="button" class="btn-cancelar" @click="cerrar">Cancelar</button>
        <button
          type="button"
          class="btn-confirmar"
          @click="borrarUsuario"
        >
          Borrar
        </button>
      </footer>
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
  max-width: 480px;
  padding: 28px 28px 24px;
  background-color: #ffffff;
  border-radius: 14px;
  box-shadow: 0 20px 50px rgba(15, 23, 42, 0.25);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

.modal-header {
  margin-bottom: 14px;
}

.modal-titulo {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: #0f172a;
}

.modal-correo {
  color: #2563eb;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
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

.btn-confirmar {
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 600;
  color: #ffffff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  background-color: #dc2626;
}
</style>