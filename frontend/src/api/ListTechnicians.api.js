import axios from "axios";

export const getLisTechnicians = () => {
  try {
    const response = axios.get("http://localhost:8000/api/technicians/list/");
    return response;
  } catch (error) {
    console.error(error);
  }
};
