import axios from "axios";

export const getListSchemas = () => {
  try {
    const response = axios.get("http://localhost:8000/api/schemas/");
    return response;
  } catch (error) {
    console.error(error);
  }
};
