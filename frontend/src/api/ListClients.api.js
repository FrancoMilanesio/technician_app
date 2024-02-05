import axios from "axios";

export const getLisClients = () => {
  try {
    const response = axios.get("http://localhost:8000/api/clients/list/");
    return response;
  } catch (error) {
    console.error(error);
  }
};
