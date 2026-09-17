<script setup>
import { ref, watch } from 'vue'
import api from '@/services/axios'

const props = defineProps({
  mostrar: {
    type: Boolean,
    default: false,
  },
  posicionInicial: {
    type: Object,
    default: () => ({ x: 24, y: 24 }),
  },
})

const emit = defineEmits(['cerrar', 'creada'])

const titulo = ref('')
const texto = ref('')

function resetearFormulario() {
  titulo.value = ''
  texto.value = ''
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

const crearNota = async () => {
  const token = localStorage.getItem('access')
  try {
    const response = await api.post('/notas/notas/', {
        titulo: titulo.value,
        texto: texto.value,
        posicion_x: props.posicionInicial.x,
        posicion_y: props.posicionInicial.y,
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    console.log('Nota creada exitosamente:', response.data)
    emit('creada', response.data)
    alert('Nota creada exitosamente.')
    cerrar()
  } catch (error) {
    console.error('Error al crear nota:', error)
    alert('Error al crear nota. Verifica los datos e inténtalo nuevamente.')
  }
}

</script>

<template>
  <div v-if="mostrar" class="modal-overlay" @click.self="cerrar">
    <section class="modal-card" role="dialog" aria-modal="true" aria-labelledby="titulo-nueva-nota">
      <header class="modal-header">
        <h2 id="titulo-nueva-nota" class="modal-titulo">Nueva nota</h2>
        <button type="button" class="modal-cerrar" aria-label="Cerrar" @click="cerrar">
          &times;
        </button>
      </header>

      <form class="modal-form" @submit.prevent="crearNota">
        <section class="campo">
          <label for="titulo">Título</label>
          <input id="titulo" v-model="titulo" type="text" placeholder="Revisar propuesta del cliente" required />
        </section>

        <section class="campo">
          <label for="descripcion">Texto / Descripción</label>
          <textarea
            id="descripcion"
            v-model="texto"
            placeholder="Preparar la propuesta detallada para la reunión del viernes."
            rows="4"
            required
          ></textarea>
        </section>

        <footer class="modal-footer">
          <button type="button" class="btn-cancelar" @click="cerrar">Cancelar</button>
          <button type="submit" class="btn-crear">Crear nota</button>
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
  max-width: 540px;
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
  margin-bottom: 22px;
}

.modal-titulo {
  margin: 0;
  font-size: 22px;
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

.modal-form {
  display: flex;
  flex-direction: column;
}

.campo {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 18px;
}

.campo label {
  font-size: 13px;
  font-weight: 600;
  color: #0f172a;
}

.campo input,
.campo textarea,
.campo select {
  padding: 10px 14px;
  font-size: 14px;
  font-family: inherit;
  color: #0f172a;
  background-color: #eef1fd;
  border: 1px solid transparent;
  border-radius: 8px;
  outline: none;
  box-sizing: border-box;
}

.campo textarea {
  resize: vertical;
  min-height: 90px;
}

.campo select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20' fill='%2364748b'%3E%3Cpath fill-rule='evenodd' d='M5.23 7.21a.75.75 0 011.06.02L10 11.293l3.71-4.06a.75.75 0 111.08 1.04l-4.24 4.65a.75.75 0 01-1.08 0L5.21 8.27a.75.75 0 01.02-1.06z' clip-rule='evenodd'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 18px;
  padding-right: 36px;
  cursor: pointer;
}

.campo input::placeholder,
.campo textarea::placeholder {
  color: #94a3b8;
}

.campo input:focus,
.campo textarea:focus,
.campo select:focus {
  border-color: #2f4fe0;
  background-color: #ffffff;
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
  color: #1d3fd6;
  background-color: #e2e9fb;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.btn-cancelar:hover {
  background-color: #d3dcf8;
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