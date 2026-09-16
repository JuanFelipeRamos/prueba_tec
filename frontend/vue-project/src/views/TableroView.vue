<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import NotaCardComponent from '@/components/NotaCardComponent.vue'
import NavbarComponent from '@/components/NavbarComponent.vue'

const token = ref(localStorage.getItem('access'))
const router = useRouter()

onMounted(() => {
  if (!token.value) {
    alert('No se encontró token de acceso. Redirigiendo a la página de inicio de sesión.')
    router.push('/')
  }
})

const emit = defineEmits(['mover-nota', 'guardar-nota', 'eliminar-nota', 'nueva-nota'])

const notas = ref([
  {
    id: 1,
    titulo: 'Revisar propuesta del cliente',
    descripcion: 'Preparar la propuesta para la reunión del viernes con el equipo de operaciones.',
    estado: 'pendiente',
    x: 20,
    y: 20,
  },
  {
    id: 2,
    titulo: 'Actualizar documentación',
    descripcion: 'Revisar y actualizar la documentación del proyecto y la API en Django.',
    estado: 'en_curso',
    x: 380,
    y: 30,
  },
  {
    id: 3,
    titulo: 'Enviar informe',
    descripcion: 'Enviar el informe final al equipo de dirección.',
    estado: 'hecho',
    x: 740,
    y: 45,
  },
  {
    id: 4,
    titulo: 'Configurar base de datos MySQL',
    descripcion: 'Verificar índices y backups automáticos del servidor.',
    estado: 'pendiente',
    x: 60,
    y: 340,
  },
  {
    id: 5,
    titulo: 'Pruebas de endpoints REST',
    descripcion: 'Validar autenticación por token y permisos de administrador.',
    estado: 'en_curso',
    x: 440,
    y: 360,
  },
  {
    id: 6,
    titulo: 'Diseño de arquitectura inicial',
    descripcion: 'Definir entidades Usuario, Rol y Nota para el equipo.',
    estado: 'hecho',
    x: 800,
    y: 320,
  },
])

const totalNotas = computed(() => notas.value.length)
const contadorPendientes = computed(() => notas.value.filter((n) => n.estado === 'pendiente').length)
const contadorEnCurso = computed(() => notas.value.filter((n) => n.estado === 'en_curso').length)
const contadorHechas = computed(() => notas.value.filter((n) => n.estado === 'hecho').length)

function onMoverNota({ id, x, y }) {
  const nota = notas.value.find((n) => n.id === id)
  if (nota) {
    nota.x = x
    nota.y = y
  }
  emit('mover-nota', { id, x, y })
}

function onGuardarNota({ id, estado }) {
  const nota = notas.value.find((n) => n.id === id)
  if (nota) {
    nota.estado = estado
  }
  emit('guardar-nota', { id, estado })
}

function onEliminarNota(id) {
  notas.value = notas.value.filter((n) => n.id !== id)
  emit('eliminar-nota', id)
}

function crearNota() {
  emit('nueva-nota')
}
</script>

<template>
  <main class="tablero-page">
    <NavbarComponent />
    <header class="tablero-header">
      <h1 class="tablero-title">Tablero de notas</h1>
      <button type="button" class="btn-nueva-nota" @click="crearNota">
        + Nueva nota
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

    <section class="tablero-lienzo">
      <NotaCardComponent
        v-for="nota in notas"
        :key="nota.id"
        :nota="nota"
        @mover="onMoverNota"
        @guardar="onGuardarNota"
        @eliminar="onEliminarNota"
      />
    </section>
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