<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  nota: {
    type: Object,
    required: true,
    // Forma esperada: { id, titulo, descripcion, estado, x, y }
  },
})

const emit = defineEmits(['mover', 'guardar', 'eliminar'])

// Posición local propia del componente para que el arrastre se sienta fluido;
// se sincroniza si el padre cambia la posición desde afuera (por ejemplo tras
// recibir la respuesta de la API).
const posX = ref(props.nota.x)
const posY = ref(props.nota.y)

watch(
  () => [props.nota.x, props.nota.y],
  ([nuevoX, nuevoY]) => {
    posX.value = nuevoX
    posY.value = nuevoY
  }
)

const estadoSeleccionado = ref(props.nota.estado)

const etiquetas = {
  pendiente: 'PENDIENTE',
  en_curso: 'EN CURSO',
  hecho: 'HECHO',
}

const etiquetaEstado = computed(() => etiquetas[props.nota.estado] || '')
const claseEstado = computed(() => `nota-card--${props.nota.estado}`)

const estiloPosicion = computed(() => ({
  left: `${posX.value}px`,
  top: `${posY.value}px`,
}))

let arrastrando = false
let inicioPuntero = { x: 0, y: 0 }
let inicioPosicion = { x: 0, y: 0 }

function iniciarArrastre(evento) {
  arrastrando = true
  inicioPuntero = { x: evento.clientX, y: evento.clientY }
  inicioPosicion = { x: posX.value, y: posY.value }
  window.addEventListener('pointermove', moverArrastre)
  window.addEventListener('pointerup', finalizarArrastre)
}

function moverArrastre(evento) {
  if (!arrastrando) return
  const deltaX = evento.clientX - inicioPuntero.x
  const deltaY = evento.clientY - inicioPuntero.y
  posX.value = inicioPosicion.x + deltaX
  posY.value = inicioPosicion.y + deltaY
}

function finalizarArrastre() {
  if (!arrastrando) return
  arrastrando = false
  window.removeEventListener('pointermove', moverArrastre)
  window.removeEventListener('pointerup', finalizarArrastre)
  // El padre (o la vista del tablero) es responsable de llamar a la API
  // para persistir esta nueva posición.
  emit('mover', { id: props.nota.id, x: posX.value, y: posY.value })
}

function guardarCambios() {
  emit('guardar', { id: props.nota.id, estado: estadoSeleccionado.value })
}
</script>

<template>
  <article
    class="nota-card"
    :class="claseEstado"
    :style="estiloPosicion"
    @pointerdown="iniciarArrastre"
  >
    <header class="nota-card__header">
      <span class="nota-card__etiqueta">{{ etiquetaEstado }}</span>
    </header>

    <section class="nota-card__cuerpo">
      <h2 class="nota-card__titulo">{{ nota.titulo }}</h2>
      <p class="nota-card__descripcion">{{ nota.descripcion }}</p>
    </section>

    <footer class="nota-card__footer" @pointerdown.stop>
      <select v-model="estadoSeleccionado" class="nota-card__select">
        <option value="pendiente">Pendiente</option>
        <option value="en_curso">En curso</option>
        <option value="hecho">Hecho</option>
      </select>

      <button type="button" class="nota-card__eliminar" @click="$emit('eliminar', nota.id)">
        Eliminar
      </button>

      <button type="button" class="nota-card__guardar" @click="guardarCambios">
        Guardar
      </button>
    </footer>
  </article>
</template>

<style scoped>
.nota-card {
  position: absolute;
  width: 320px;
  border-radius: 10px;
  padding: 16px;
  cursor: grab;
  user-select: none;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

.nota-card:active {
  cursor: grabbing;
}

.nota-card--pendiente {
  background-color: #fdf3c7;
}

.nota-card--en_curso {
  background-color: #dce8fd;
}

.nota-card--hecho {
  background-color: #d3f3e2;
}

.nota-card__header {
  padding-bottom: 10px;
  margin-bottom: 10px;
  border-bottom: 1px solid rgba(15, 23, 42, 0.1);
}

.nota-card__etiqueta {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.nota-card--pendiente .nota-card__etiqueta {
  color: #92400e;
}

.nota-card--en_curso .nota-card__etiqueta {
  color: #1e3a8a;
}

.nota-card--hecho .nota-card__etiqueta {
  color: #065f46;
}

.nota-card__cuerpo {
  min-height: 70px;
  margin-bottom: 16px;
}

.nota-card__titulo {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: 700;
  color: #0f172a;
}

.nota-card__descripcion {
  margin: 0;
  font-size: 13px;
  line-height: 1.5;
  color: #334155;
}

.nota-card__footer {
  display: flex;
  align-items: center;
  gap: 10px;
}

.nota-card__select {
  padding: 6px 10px;
  font-size: 13px;
  color: #0f172a;
  background-color: #ffffff;
  border: 1px solid rgba(15, 23, 42, 0.15);
  border-radius: 6px;
  outline: none;
  cursor: pointer;
}

.nota-card__eliminar {
  margin-left: auto;
  padding: 0;
  font-size: 13px;
  font-weight: 600;
  color: #dc2626;
  background: none;
  border: none;
  cursor: pointer;
}

.nota-card__eliminar:hover {
  text-decoration: underline;
}

.nota-card__guardar {
  padding: 6px 14px;
  font-size: 13px;
  font-weight: 600;
  color: #ffffff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.nota-card--pendiente .nota-card__guardar {
  background-color: #d97706;
}

.nota-card--pendiente .nota-card__guardar:hover {
  background-color: #b45f04;
}

.nota-card--en_curso .nota-card__guardar {
  background-color: #2563eb;
}

.nota-card--en_curso .nota-card__guardar:hover {
  background-color: #1d4ed8;
}

.nota-card--hecho .nota-card__guardar {
  background-color: #059669;
}

.nota-card--hecho .nota-card__guardar:hover {
  background-color: #047857;
}
</style>