import axios from "axios";

export const updateOrder = async (
  order_id,
  client_id,
  technician,
  hours_worked,
  type_request,
  scheme_id,
  setLoading,
  setBackdrop
) => {
  setLoading(true);
  setBackdrop(true);
  try {
    const response = await axios.put(
      "http://localhost:8000/api/order/update/",
      {
        order_id,
        client_id,
        technician,
        hours_worked,
        type_request,
        scheme_id,
      }
    );
    setLoading(false);
    setBackdrop(false);
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
};
