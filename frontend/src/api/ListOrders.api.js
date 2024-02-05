import axios from "axios";

export const getListOrders = () => {
  try {
    const response = axios.get("http://localhost:8000/api/orders/");
    return response;
  } catch (error) {
    console.error(error);
  }
};
