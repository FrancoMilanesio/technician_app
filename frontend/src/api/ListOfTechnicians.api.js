import axios from "axios";

export const getListOfTechnicians = () => {
  try {
    const response = axios.get("http://localhost:8000/api/technical/");
    return response;
  } catch (error) {
    console.error(error);
  }
};
