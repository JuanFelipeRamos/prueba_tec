<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router';
import api from '@/services/axios'

const username = ref('')
const password = ref('')
const router = useRouter()

const login = async () => {
  try {
    const response = await api.post('/token/', {
      username: username.value,
      password: password.value,
    })

    localStorage.setItem('access', response.data.access)
    console.log('inicio de sesión exitoso')
    router.push('/tablero')
  } catch (error) {
        alert('Error al iniciar sesión, credenciales inválidas o usuario inactivo.')
        if (error.response) {
            console.error("Detalles del error del servidor:", error.response.data);
        } else {
            console.error("Error desconocido:", error.message);
        }
    }
}

</script>

<template>
  <main class="login-page">
    <section class="login-card">
      <header>
        <h1 class="login-title">Portal de Equipo</h1>
      </header>

      <form class="login-form" @submit.prevent="login">
        <section class="form-group">
          <label for="email" class="form-label">Nombre de usuario</label>
          <input
            id="username"
            v-model="username"
            type="text"
            class="form-input"
            required
            placeholder="ej. carlos@empresa.com"
            autocomplete="username"
          />
        </section>

        <section class="form-group">
          <label for="password" class="form-label">Contraseña</label>
          <input
            id="password"
            v-model="password"
            type="password"
            class="form-input"
            required
            placeholder="••••••••"
            autocomplete="current-password"
          />
        </section>

        <button type="submit" class="submit-btn">Iniciar sesión</button>
      </form>
    </section>
  </main>
</template>

<style scoped>
.login-page {
  min-height: 100vh;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f6fd;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

.login-card {
  width: 100%;
  max-width: 400px;
  background-color: #ffffff;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 10px 30px rgba(17, 24, 39, 0.06);
}

.login-title {
  margin: 0 0 24px 0;
  font-size: 24px;
  font-weight: 700;
  color: #0f172a;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: 14px;
  font-weight: 500;
  color: #0f172a;
}

.form-input {
  width: 100%;
  box-sizing: border-box;
  padding: 10px 14px;
  font-size: 14px;
  color: #0f172a;
  background-color: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  outline: none;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.form-input::placeholder {
  color: #b7bdc9;
}

.form-input:focus {
  border-color: #0047d6;
  box-shadow: 0 0 0 3px rgba(0, 71, 214, 0.12);
}

.submit-btn {
  width: 100%;
  padding: 12px 14px;
  margin-top: 4px;
  font-size: 15px;
  font-weight: 600;
  color: #ffffff;
  background-color: #0047d6;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.submit-btn:hover {
  background-color: #003bb3;
}
</style>