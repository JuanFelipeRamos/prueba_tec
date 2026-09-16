import api from '@/services/axios'

export const obtenerPerfilUsuario = async () => {
    try {
        const token = localStorage.getItem('access');
        if (!token) {
            console.error('No se encontró el token de acceso.');
            return;
        }

        const response = await api.get('/usuarios/usuarios/me/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.data) {
            console.error('Error al obtener el perfil del usuario.');
            return;
        }

        const userData = response.data;
        return userData;
    } catch (error) {
        console.error('Error al obtener el perfil del usuario:', error);
    }
}
