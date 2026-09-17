<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import NavbarComponent from '@/components/NavbarComponent.vue'
import DashboardEstadisticas from '@/components/DashboardEstadisticas.vue'
import api from '@/services/axios'

const token = ref(localStorage.getItem('access'))
const router = useRouter()

const totalNotas = ref(0)
const pendientes = ref(0)
const enCurso = ref(0)
const hechas = ref(0)
const cargando = ref(true)

const obtenerMetricas = async () => {
  try {
    const response = await api.get('/notas/metricas/', {
      headers: {
        Authorization: `Bearer ${token.value}`,
      },
    })

    totalNotas.value = response.data.total
    pendientes.value = response.data.pendientes
    enCurso.value = response.data.en_curso
    hechas.value = response.data.hechas
  } catch (error) {
    console.error('Error al obtener las métricas del dashboard:', error)
    alert('Error al obtener las métricas del dashboard. Inténtalo nuevamente.')
  } finally {
    cargando.value = false
  }
}

onMounted(() => {
  obtenerMetricas()
  if (!token.value) {
    alert('No se encontró token de acceso. Redirigiendo a la página de inicio de sesión.')
    router.push('/')
  }
})
</script>

<template>
  <main class="dashboard-view">
    <NavbarComponent />

    <DashboardEstadisticas
      v-if="!cargando"
      :total-notas="totalNotas"
      :pendientes="pendientes"
      :en-curso="enCurso"
      :hechas="hechas"
    />
  </main>
</template>

<style scoped>
.dashboard-view {
  min-height: 100%;
}
</style>