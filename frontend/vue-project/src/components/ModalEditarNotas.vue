<script setup>
import { ref, computed, watch } from 'vue'
import api from '@/services/axios'

const props = defineProps({
	mostrar: {
		type: Boolean,
		default: false,
	},
	nota: {
		type: Object,
		default: null,
	},
})

const emit = defineEmits(['cerrar', 'editado'])

const titulo = ref('')
const texto = ref('')

function resetearFormulario() {
	titulo.value = props.nota?.titulo || ''
	texto.value = props.nota?.texto || props.nota?.descripcion || ''
}

watch(
	() => [props.mostrar, props.nota],
	([visible]) => {
		if (visible) {
			resetearFormulario()
		}
	}
)

const hayCambios = computed(() => {
	return Boolean(props.nota) && (
		titulo.value.trim() !== (props.nota.titulo || '') ||
		texto.value.trim() !== (props.nota.texto || props.nota.descripcion || '')
	)
})

function cerrar() {
	emit('cerrar')
}

function detalleError(error) {
	return Object.values(error.response?.data ?? {}).flat().join(' ')
}

const editarNota = async () => {
	if (!hayCambios.value || !props.nota) return

	const cambios = {
		titulo: titulo.value.trim(),
		texto: texto.value.trim(),
	}

	try {
		const response = await api.patch(`/notas/notas/${props.nota.id}/`, cambios)
		alert('Nota editada exitosamente.')
		emit('editado', response.data)
		cerrar()
	} catch (error) {
		console.error('Error al editar nota:', error)
		alert(detalleError(error) || 'Error al editar nota. Verifica los datos e inténtalo nuevamente.')
	}
}
</script>

<template>
	<div v-if="mostrar" class="modal-overlay" @click.self="cerrar">
		<section class="modal-card" role="dialog" aria-modal="true" aria-labelledby="titulo-editar-nota">
			<header class="modal-header">
				<h2 id="titulo-editar-nota" class="modal-titulo">Editar nota</h2>
				<button type="button" class="modal-cerrar" aria-label="Cerrar" @click="cerrar">&times;</button>
			</header>

			<form class="modal-form" @submit.prevent="editarNota">
				<section class="campo">
					<label for="titulo-nota">Título</label>
					<input id="titulo-nota" v-model="titulo" type="text" required />
				</section>

				<section class="campo">
					<label for="texto-nota">Texto / Descripción</label>
					<textarea id="texto-nota" v-model="texto" rows="5" required></textarea>
				</section>

				<footer class="modal-footer">
					<button type="button" class="btn-cancelar" @click="cerrar">Cancelar</button>
					<button type="submit" class="btn-editar" :disabled="!hayCambios">Editar nota</button>
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
	margin-bottom: 22px;
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

.campo label {
	font-size: 13px;
	font-weight: 600;
	color: #0f172a;
}

.campo input,
.campo textarea {
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
}

.campo input:focus,
.campo textarea:focus {
	border-color: #2f4fe0;
	background-color: #ffffff;
}

.modal-footer {
	display: flex;
	justify-content: flex-end;
	gap: 12px;
}

.btn-cancelar,
.btn-editar {
	padding: 10px 20px;
	font-size: 14px;
	font-weight: 600;
	border: none;
	border-radius: 8px;
	cursor: pointer;
}

.btn-cancelar {
	color: #1d3fd6;
	background-color: #e2e9fb;
}

.btn-editar {
	color: #ffffff;
	background-color: #2f4fe0;
}

.btn-editar:disabled {
	opacity: 0.5;
	cursor: not-allowed;
}
</style>
