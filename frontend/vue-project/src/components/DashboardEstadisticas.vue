<script setup>
import { computed } from 'vue'

const props = defineProps({
  totalNotas: {
    type: Number,
    default: 12,
  },
  pendientes: {
    type: Number,
    default: 5,
  },
  enCurso: {
    type: Number,
    default: 4,
  },
  hechas: {
    type: Number,
    default: 3,
  },
})

function calcularPorcentaje(cantidad) {
  if (!props.totalNotas) return '0.0'
  return ((cantidad / props.totalNotas) * 100).toFixed(1)
}

const porcentajePendientes = computed(() => calcularPorcentaje(props.pendientes))
const porcentajeEnCurso = computed(() => calcularPorcentaje(props.enCurso))
const porcentajeHechas = computed(() => calcularPorcentaje(props.hechas))
</script>

<template>
  <main class="dashboard-page">
    <header class="dashboard-header">
      <h1 class="dashboard-title">Resumen de notas del equipo</h1>
    </header>

    <section class="dashboard-stats">
      <article class="stat-card">
        <span class="stat-label">Total de notas</span>
        <span class="stat-numero">{{ totalNotas }}</span>
        <span class="stat-descripcion">Notas en el tablero</span>
      </article>

      <article class="stat-card">
        <span class="stat-label">Pendientes</span>
        <span class="stat-fila">
          <span class="stat-numero">{{ pendientes }}</span>
          <span class="stat-porcentaje stat-porcentaje--pendiente">{{ porcentajePendientes }}%</span>
        </span>
        <span class="stat-descripcion">Por iniciar</span>
      </article>

      <article class="stat-card">
        <span class="stat-label">En curso</span>
        <span class="stat-fila">
          <span class="stat-numero">{{ enCurso }}</span>
          <span class="stat-porcentaje stat-porcentaje--en-curso">{{ porcentajeEnCurso }}%</span>
        </span>
        <span class="stat-descripcion">En desarrollo</span>
      </article>

      <article class="stat-card">
        <span class="stat-label">Hechas</span>
        <span class="stat-fila">
          <span class="stat-numero">{{ hechas }}</span>
          <span class="stat-porcentaje stat-porcentaje--hecha">{{ porcentajeHechas }}%</span>
        </span>
        <span class="stat-descripcion">Finalizadas</span>
      </article>
    </section>
  </main>
</template>

<style scoped>
.dashboard-page {
  min-height: 100%;
  background-color: #f5f6fd;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

.dashboard-header {
  padding: 24px 32px 20px;
}

.dashboard-title {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: #0f172a;
}

.dashboard-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin: 0 32px 32px;
}

.stat-card {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
}

.stat-label {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: #64748b;
}

.stat-fila {
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.stat-numero {
  font-size: 30px;
  font-weight: 700;
  color: #0f172a;
  line-height: 1;
}

.stat-porcentaje {
  font-size: 13px;
  font-weight: 700;
}

.stat-porcentaje--pendiente {
  color: #b45309;
}

.stat-porcentaje--en-curso {
  color: #1d4ed8;
}

.stat-porcentaje--hecha {
  color: #047857;
}

.stat-descripcion {
  font-size: 13px;
  color: #64748b;
}

@media (max-width: 900px) {
  .dashboard-stats {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 520px) {
  .dashboard-stats {
    grid-template-columns: 1fr;
  }
}
</style>