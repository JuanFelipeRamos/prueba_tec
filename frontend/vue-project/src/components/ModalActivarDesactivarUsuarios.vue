<script setup>
import { computed } from 'vue'

const props = defineProps({
  mostrar: {
    type: Boolean,
    default: false,
  },
  usuario: {
    type: Object,
    default: null,
  },
  accion: {
    type: String,
    default: 'desactivar',
  },
})

const emit = defineEmits(['cerrar', 'confirmar'])

const titulo = computed(() =>
  props.accion === 'desactivar'
    ? '¿Deseas desactivar a este usuario?'
    : '¿Deseas activar a este usuario?'
)

const mensajeConsecuencia = computed(() =>
  props.accion === 'desactivar'
    ? 'no podrá iniciar sesión mientras esté inactivo.'
    : 'podrá volver a iniciar sesión en el portal.'
)

function cerrar() {
  emit('cerrar')
}

function confirmar() {
  emit('confirmar', props.usuario)
}
</script>

<template>
  <div v-if="mostrar" class="modal-overlay" @click.self="cerrar">
    <section class="modal-card" role="dialog" aria-modal="true" aria-labelledby="titulo-confirmar-estado">
      <header class="modal-header">
        <h2 id="titulo-confirmar-estado" class="modal-titulo">{{ titulo }}</h2>
      </header>

      <p class="modal-texto">
        El usuario "<strong>{{ usuario?.username }}</strong>"
        (<span class="modal-correo">{{ usuario?.email }}</span>)
        {{ mensajeConsecuencia }}
      </p>

      <footer class="modal-footer">
        <button type="button" class="btn-cancelar" @click="cerrar">Cancelar</button>
        <button
          type="button"
          class="btn-confirmar"
          :class="accion === 'desactivar' ? 'btn-confirmar--desactivar' : 'btn-confirmar--activar'"
          @click="confirmar"
        >
          {{ accion === 'desactivar' ? 'Desactivar' : 'Activar' }}
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

.modal-texto {
  margin: 0 0 22px;
  font-size: 14px;
  line-height: 1.6;
  color: #334155;
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
}

.btn-confirmar--desactivar {
  background-color: #dc2626;
}

.btn-confirmar--desactivar:hover {
  background-color: #b91c1c;
}

.btn-confirmar--activar {
  background-color: #2f4fe0;
}

.btn-confirmar--activar:hover {
  background-color: #2440c2;
}
</style>