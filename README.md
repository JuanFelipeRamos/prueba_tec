# 📋 Tablero de Notas - Prueba Técnica

Este proyecto es una aplicación web para la gestión de notas, desarrollada con **Django Rest Framework** en el backend y **Vue.js (Vite)** en el frontend, utilizando **MySQL** como base de datos local.

---

## 🛠️ Instrucciones de Instalación y Uso Local

### 1. Requisitos Previos
Asegúrate de tener instalado en tu sistema:
* Python 3.12+
* Node.js (versión 18 o superior)
* Servidor MySQL activo (XAMPP, MySQL Installer, Workbench, etc.)

---

### 2. Configuración del Backend (Django)

1. Abre una terminal y navega a la carpeta del backend:
   ```bash
   cd backend
   ```
2. Crea e activa tu entorno virtual:
   ```bash
   python -m venv env
   # En Windows (PowerShell):
   .\env\Scripts\Activate.ps1
   # En Mac/Linux:
   source env/bin/activate
   ```
3. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```
4. **Archivo de Entorno (`.env`)**: Crea un archivo llamado `.env` en la raíz de la carpeta `backend/` para proteger tus credenciales locales de MySQL:
   ```ini
   DB_NAME=tablero_notas_db
   DB_USER=root
   DB_PASSWORD=tu_contraseña_mysql
   DB_HOST=localhost
   DB_PORT=3306
   ```
5. **Base de Datos**: Crea una base de datos vacía en tu gestor MySQL local llamada `tablero_notas_db`.
6. Ejecuta las migraciones para estructurar las tablas:
   ```bash
   python manage.py migrate
   ```
7. **Creación de Acceso**: Crea tu usuario administrador local para poder interactuar con el sistema:
   ```bash
   python manage.py createsuperuser
   ```
8. Inicia el servidor de desarrollo del backend:
   ```bash
   python manage.py runserver
   ```

---

### 3. Configuración del Frontend (Vue 3)

1. Abre una segunda terminal y navega a la carpeta del frontend:
   ```bash
   cd frontend/vue-project
   ```
2. Instala los paquetes y dependencias de Node:
   ```bash
   npm install
   ```
3. Inicia el servidor de desarrollo de Vite:
   ```bash
   npm run dev
   ```

Una vez encendidos ambos servicios, podrás ingresar al panel de administración de Django en `http://127.0.0` y abrir la interfaz de usuario de Vue en la URL local provista por Vite (usualmente `http://localhost:5173`).

---

## 📢 Nota del Desarrollador (Sobre requerimientos pendientes)

El proyecto incluye el **CRUD completo y funcional** de notas y la gestión de usuarios por roles, con su correspondiente consumo e integración desde la interfaz visual en Vue 3. 

Por cuestiones estrictas de tiempo de entrega, **no se implementó la arquitectura en contenedores con Docker Compose ni las simulaciones de servicios con AWS Lambda**. Actualmente no he integrado estas herramientas específicas (`Docker`, `AWS SAM`, `CloudFormation`) en mis flujos de desarrollo cotidianos. 

No obstante, **cuento con una total disposición, entusiasmo y facilidad de aprendizaje** para adaptarme rápidamente a este stack tecnológico y cubrir cualquier necesidad técnica que la empresa requiera a la brevedad.
