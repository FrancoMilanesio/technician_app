import axios from 'axios';

export const getTechniciansReport = () => { 
    try {
        const response = axios.get('http://localhost:8000/api/technical/report/');
        return response;
    } catch (error) {
        console.error(error);
    }
};