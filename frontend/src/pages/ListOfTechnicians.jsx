import { useEffect, useState } from "react";
import * as React from "react";
import { getListOfTechnicians } from "../api/ListOfTechnicians.api";
import Pagination from "@mui/material/Pagination";
import Stack from "@mui/material/Stack";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import Divider from "@mui/material/Divider";
import ListItemText from "@mui/material/ListItemText";
import ListItemAvatar from "@mui/material/ListItemAvatar";
import Avatar from "@mui/material/Avatar";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";

export function ListOfTechnicians() {
  const [technicians, setTechnicians] = useState([]);
  const [page, setPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(10);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    const fetchTechnicians = async () => {
      const techniciansData = await getListOfTechnicians();
      setTechnicians(techniciansData.data);
    };

    fetchTechnicians();
  }, []);

  const handleChangePage = (event, value) => {
    setPage(value);
  };

  const startIndex = (page - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;

  const filteredTechnicians = technicians.filter((technical) =>
    technical.full_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <Typography variant="h4" gutterBottom>
        LISTADO DE TÉCNICOS
      </Typography>
      <TextField
        label="Buscar por nombre"
        variant="outlined"
        onChange={(e) => setSearchTerm(e.target.value)}
        style={{ marginBottom: "20px" }}
      />
      <List
        sx={{
          width: "100%",
          maxWidth: 690,
          margin: "auto",
          bgcolor: "background.paper",
          justifyContent: "center",
        }}
      >
        {filteredTechnicians
          .slice(startIndex, endIndex)
          .map((technical, index) => (
            <React.Fragment key={index}>
              <ListItem alignItems="flex-start">
                <ListItemAvatar>
                  <Avatar
                    alt={technical.full_name}
                    src={`/static/images/avatar/${index + 1}.jpg`}
                  />
                </ListItemAvatar>
                <ListItemText
                  primary={technical.full_name}
                  secondary={
                    <React.Fragment>
                      <Typography
                        sx={{ display: "inline" }}
                        component="span"
                        variant="body2"
                        color="text.primary"
                      >
                        {technical.category}
                      </Typography>
                      {` — Total de horas trabajadas: ${technical.total_hours_worked}hs, Monto total: $${technical.hours_worked_total_amount}, Cantidad de pedidos: ${technical.orders_cuantity}`}
                    </React.Fragment>
                  }
                />
              </ListItem>
              {index !== itemsPerPage - 1 && (
                <Divider variant="inset" component="li" />
              )}
            </React.Fragment>
          ))}
      </List>
      <Stack>
        <Pagination
          sx={{ display: "flex", justifyContent: "center", marginTop: "20px" }}
          count={Math.ceil(filteredTechnicians.length / itemsPerPage)}
          page={page}
          onChange={handleChangePage}
        />
      </Stack>
    </div>
  );
}
