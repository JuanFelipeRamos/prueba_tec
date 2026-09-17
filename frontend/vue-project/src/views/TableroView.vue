<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { obtenerNotas } from '@/services/obtenerNotas'
import api from '@/services/axios'
import NotaCardComponent from '@/components/NotaCardComponent.vue'
import NavbarComponent from '@/components/NavbarComponent.vue'
import ModalCrearNota from '@/components/ModalCrearNota.vue'
import ModalEditarNotas from '@/components/ModalEditarNotas.vue'

const token = ref(localStorage.getItem('access'))
const router = useRouter()
const listadoNotas = ref([])
const lienzo = ref(null)
const notaEnEdicion = ref(null)
const mostrarModalEditar = ref(false)

const ANCHO_NOTA = 320
const ALTO_NOTA = 220
const SEPARACION = 24

function adaptarNota(nota) {
  return {
    ...nota,
    descripcion: nota.texto,
    estado: nota.estado === 'en curso' ? 'en_curso' : nota.estado,
    x: nota.posicion_x ?? 24,
    y: nota.posicion_y ?? 24,
  }
}

// obtener la lista de notas
const obtenerNotasData = async () => {
  const notasData = await obtenerNotas()
  listadoNotas.value = (notasData ?? []).map(adaptarNota)
}

onMounted(() => {
  obtenerNotasData()
  if (!token.value) {
    alert('No se encontró token de acceso. Redirigiendo a la página de inicio de sesión.')
    router.push('/')
  }
})

const emit = defineEmits(['mover-nota', 'guardar-nota', 'eliminar-nota', 'nueva-nota'])

const totalNotas = computed(() => listadoNotas.value.length)
const contadorPendientes = computed(() => listadoNotas.value.filter((n) => n.estado === 'pendiente').length)
const contadorEnCurso = computed(() => listadoNotas.value.filter((n) => n.estado === 'en_curso').length)
const contadorHechas = computed(() => listadoNotas.value.filter((n) => n.estado === 'hecho').length)

function onMoverNota({ id, x, y }) {
  const nota = listadoNotas.value.find((n) => n.id === id)
  if (nota) {
    const anchoDisponible = lienzo.value?.clientWidth ?? ANCHO_NOTA
    const altoDisponible = lienzo.value?.clientHeight ?? ALTO_NOTA
    nota.x = Math.max(0, Math.min(x, anchoDisponible - ANCHO_NOTA))
    nota.y = Math.max(0, Math.min(y, altoDisponible - ALTO_NOTA))

    api.patch(`/notas/notas/${id}/`, {
      posicion_x: nota.x,
      posicion_y: nota.y,
    }).catch((error) => console.error('Error al guardar la posición:', error))
  }
  emit('mover-nota', { id, x: nota?.x ?? x, y: nota?.y ?? y })
}

function onGuardarNota({ id, estado }) {
  const nota = listadoNotas.value.find((n) => n.id === id)
  if (nota) {
    nota.estado = estado
    api.patch(`/notas/notas/${id}/`, {
      estado: estado === 'en_curso' ? 'en curso' : estado,
    }).catch((error) => console.error('Error al guardar el estado:', error))
  }
  emit('guardar-nota', { id, estado })
}

function onEditarNota(id) {
  notaEnEdicion.value = listadoNotas.value.find((nota) => nota.id === id) || null
  mostrarModalEditar.value = Boolean(notaEnEdicion.value)
}

function cerrarModalEditar() {
  mostrarModalEditar.value = false
  notaEnEdicion.value = null
}

function onNotaEditada(notaActualizada) {
  const indice = listadoNotas.value.findIndex((nota) => nota.id === notaActualizada.id)
  if (indice !== -1) {
    listadoNotas.value[indice] = adaptarNota(notaActualizada)
  }
  cerrarModalEditar()
}

function onEliminarNota(id) {
  listadoNotas.value = listadoNotas.value.filter((n) => n.id !== id)
  api.delete(`/notas/notas/${id}/`).catch((error) => console.error('Error al eliminar la nota:', error))
  emit('eliminar-nota', id)
}

// Modal de "Nueva nota"
const mostrarModalCrear = ref(false)

function crearNota() {
  mostrarModalCrear.value = true
}

function cerrarModalCrear() {
  mostrarModalCrear.value = false
}

function siguientePosicion() {
  const columnas = Math.max(
    1,
    Math.floor(((lienzo.value?.clientWidth ?? ANCHO_NOTA) - SEPARACION) / (ANCHO_NOTA + SEPARACION))
  )
  const indice = listadoNotas.value.length
  return {
    x: SEPARACION + (indice % columnas) * (ANCHO_NOTA + SEPARACION),
    y: SEPARACION + Math.floor(indice / columnas) * (ALTO_NOTA + SEPARACION),
  }
}

function onNotaCreada(nuevaNota) {
  listadoNotas.value.push(adaptarNota(nuevaNota))
  mostrarModalCrear.value = false
  emit('nueva-nota', nuevaNota)
}
</script>

<template>
  <main class="tablero-page">
    <NavbarComponent />
    <header class="tablero-header">
      <h1 class="tablero-title">Tablero de notas</h1>
      <button type="button" class="btn-nueva-nota" @click="crearNota">
        Nueva nota
      </button>
    </header>

    <section class="tablero-resumen">
      <span>Total: {{ totalNotas }} notas</span>
      <span class="separador">•</span>
      <span class="resumen-pendientes">{{ contadorPendientes }} pendientes</span>
      <span class="separador">•</span>
      <span class="resumen-en-curso">{{ contadorEnCurso }} en curso</span>
      <span class="separador">•</span>
      <span class="resumen-hechas">{{ contadorHechas }} hechas</span>
    </section>

    <section ref="lienzo" class="tablero-lienzo">
      <NotaCardComponent
        v-for="nota in listadoNotas"
        :key="nota.id"
        :nota="nota"
        @mover="onMoverNota"
        @guardar="onGuardarNota"
        @editar="onEditarNota"
        @eliminar="onEliminarNota"
      />
    </section>

    <ModalCrearNota
      :mostrar="mostrarModalCrear"
      :posicion-inicial="siguientePosicion()"
      @cerrar="cerrarModalCrear"
      @creada="onNotaCreada"
    />

    <ModalEditarNotas
      :mostrar="mostrarModalEditar"
      :nota="notaEnEdicion"
      @cerrar="cerrarModalEditar"
      @editado="onNotaEditada"
    />
  </main>
</template>

<style scoped>
.tablero-page {
  min-height: 100%;
  background-color: #ffffff;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

.tablero-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 28px 32px 20px;
}

.tablero-title {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #0f172a;
}

.btn-nueva-nota {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 18px;
  font-size: 14px;
  font-weight: 600;
  color: #ffffff;
  background-color: #3b5bfd;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.btn-nueva-nota:hover {
  background-color: #2f49d1;
}

.tablero-resumen {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0 32px 20px;
  padding: 14px 20px;
  font-size: 14px;
  color: #334155;
  background-color: #f2f4fc;
  border-radius: 10px;
}

.separador {
  color: #94a3b8;
}

.resumen-pendientes {
  color: #b45309;
  font-weight: 600;
}

.resumen-en-curso {
  color: #1d4ed8;
  font-weight: 600;
}

.resumen-hechas {
  color: #047857;
  font-weight: 600;
}

.tablero-lienzo {
  position: relative;
  min-height: 780px;
  margin: 0 32px 32px;
  padding: 24px;
  background-color: #ffffff;
  border: 1px solid #eef0f7;
  border-radius: 12px;
  overflow: auto;
}
</style>