import { useEffect, useState } from "react";
import { getListOfTechnicians } from "../api/ListOfTechnicians.api";

export function ListOfTechnicians() {
  const [technicians, setTechnicians] = useState([]);

  useEffect(() => {
    const fetchTechnicians = async () => {
      const techniciansData = await getListOfTechnicians();
      setTechnicians(techniciansData.data);
    };

    fetchTechnicians();
  }, []);
  
  return (
    <div>
      <h1>List of Technicians</h1>
      <ul>
        {technicians.map((technical) => {
          return (
            <li key={technical.id}>
              {technical.full_name}
            </li>
          );
        })};
      </ul>
    </div>
  );
}