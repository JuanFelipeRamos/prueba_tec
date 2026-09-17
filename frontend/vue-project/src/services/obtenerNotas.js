import api from '@/services/axios'

export const obtenerNotas = async () => {
    try {
        const token = localStorage.getItem('access');
        if (!token) {
            console.error('No se encontró el token de acceso.');
            return;
        }

        const response = await api.get('/notas/notas/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.data) {
            console.error('Error al obtener las notas.');
            return;
        }

        const notasData = response.data;
        return notasData;
    } catch (error) {
        console.error('Error al obtener las notas:', error);
    }
}
