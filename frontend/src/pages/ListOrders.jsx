import * as React from "react";
import Box from "@mui/material/Box";
import EditIcon from "@mui/icons-material/Edit";
import SaveIcon from "@mui/icons-material/Save";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import CircularProgress from "@mui/material/CircularProgress";
import Backdrop from "@mui/material/Backdrop";
import TextField from "@mui/material/TextField";
import Select, { SelectChangeEvent } from "@mui/material/Select";
import {
  DataGrid,
  GridActionsCellItem,
  GridRowEditStopReasons,
} from "@mui/x-data-grid";
import { useState, useEffect } from "react";
import { getListOrders } from "../api/ListOrders.api";
import { updateOrder } from "../api/OrderUpdate.api";
import { getLisTechnicians } from "../api/ListTechnicians.api";
import { getLisClients } from "../api/ListClients.api";
import { getListSchemas } from "../api/ListSchemas.api";

export function ListOrders() {
  const [rows, setRows] = useState([]);
  const [rowModesModel, setRowModesModel] = useState({});
  const [page, setPage] = useState(1);
  const [technicians, setTechnicians] = useState([]);
  const [selectedTechnician, setSelectedTechnician] = useState(null);
  const [clients, setClients] = useState(null);
  const [selectedClient, setSelectedClient] = useState(null);
  const [hoursWorked, setHoursWorked] = useState(null);
  const [loading, setLoading] = useState(false);
  const [backdrop, setBackdrop] = useState(false);
  const [schemas, setSchemas] = useState(null);
  const [selectedSchema, setSelectedSchema] = useState(null);
  const [selectedTypeRequest, setSelectedTypeRequest] = useState(null);

  useEffect(() => {
    const fetchOrders = async () => {
      const response = await getListOrders(page);
      const formattedRows = response.data.map((order) => ({
        id: order.id,
        order_number: order.id,
        client: `${order.client.first_name} ${order.client.last_name}`,
        client_id: order.client.id,
        scheme: order.scheme ? order.scheme.name : "--",
        scheme_id: order.scheme ? order.scheme.id : null,
        type_request: order.type_request === 1 ? "Pedido" : "Solicitud",
        type_request_id: order.type_request,
        technical: `${order.technician.first_name} ${order.technician.last_name}`,
        technical_id: order.technician.id,
        hours_worked: `${order.hours_worked}`,
      }));

      setRows(formattedRows);
    };

    const fetchTechnicians = async () => {
      try {
        const techniciansList = await getLisTechnicians();
        const TechnicianOptions = techniciansList.data.map((technician) => ({
          value: technician.id,
          label: `${technician.first_name} ${technician.last_name}`,
        }));
        setTechnicians(TechnicianOptions);
      } catch (error) {
        console.error("Error al obtener la lista de técnicos:", error);
      }
    };

    const fetchClients = async () => {
      try {
        const clientsList = await getLisClients();
        const ClientOptions = clientsList.data.map((client) => ({
          value: client.id,
          label: `${client.first_name} ${client.last_name}`,
        }));
        setClients(ClientOptions);
      } catch (error) {
        console.error("Error al obtener la lista de clientes:", error);
      }
    };

    const fetchSchemas = async () => {
      try {
        const schemasList = await getListSchemas();
        const SchemaOptions = schemasList.data.map((schema) => ({
          value: schema.id,
          label: `${schema.name}`,
        }));
        setSchemas(SchemaOptions);
      } catch (error) {
        console.error("Error al obtener la lista de esquemas:", error);
      }
    };

    fetchOrders();
    fetchTechnicians();
    fetchClients();
    fetchSchemas();
  }, [page]);

  const handleRowEditStop = (params, event) => {
    if (params.reason === GridRowEditStopReasons.rowFocusOut) {
      event.defaultMuiPrevented = true;
    }
  };

  const handleEditClick = (id) => () => {
    setRowModesModel({ ...rowModesModel, [id]: { mode: "edit" } });
  };

  const handleSaveClick = (id) => () => {
    setRowModesModel({ ...rowModesModel, [id]: { mode: "view" } });
    const editedRow = rows.find((row) => row.id === id);
    try {
      const response = updateOrder(
        editedRow.id,
        selectedClient ? selectedClient : editedRow.client_id,
        selectedTechnician ? selectedTechnician : editedRow.technical_id,
        hoursWorked ? hoursWorked : editedRow.hours_worked,
        selectedTypeRequest ? selectedTypeRequest : editedRow.type_request_id,
        selectedSchema ? selectedSchema : editedRow.scheme_id,
        setLoading,
        setBackdrop
      );
    } catch (error) {
      console.error("Error al actualizar el pedido:", error);
    }
  };
  console.log(loading);
  const handleDeleteClick = (id) => () => {
    setRows(rows.filter((row) => row.id !== id));
  };

  const handleCancelClick = (id) => () => {
    setRowModesModel({
      ...rowModesModel,
      [id]: { mode: "view", ignoreModifications: true },
    });

    const editedRow = rows.find((row) => row.id === id);
    if (editedRow.isNew) {
      setRows(rows.filter((row) => row.id !== id));
    }
  };

  const processRowUpdate = (newRow) => {
    const updatedRow = { ...newRow, isNew: false };
    setRows(rows.map((row) => (row.id === newRow.id ? updatedRow : row)));
    return updatedRow;
  };

  const handleRowModesModelChange = (newRowModesModel) => {
    setRowModesModel(newRowModesModel);
  };

  const typeRequestOptions = [
    { value: 1, label: "Pedido" },
    { value: 0, label: "Solicitud" },
  ];

  const columns = [
    { field: "order_number", headerName: "Numero de pedido", width: 249 },
    {
      field: "client",
      headerName: "Cliente",
      width: 250,
      align: "left",
      headerAlign: "left",
      editable: true,
      renderEditCell: (params) => (
        <>
          <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={selectedClient}
            label="Age"
            onChange={(event) => {
              setSelectedClient(event.target.value);
            }}
          >
            {clients.map((x) => (
              <MenuItem value={x.value}>{x.label}</MenuItem>
            ))}
          </Select>
        </>
      ),
    },
    {
      field: "scheme",
      headerName: "Esquema de pedido",
      width: 250,
      editable: true,
      renderEditCell: (params) => (
        <>
          <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={selectedSchema}
            label="Age"
            onChange={(event) => {
              setSelectedSchema(event.target.value);
            }}
          >
            {schemas.map((x) => (
              <MenuItem value={x.value}>{x.label}</MenuItem>
            ))}
          </Select>
        </>
      ),
    },
    {
      field: "type_request",
      headerName: "Tipo de pedido",
      width: 250,
      editable: true,
      renderEditCell: (params) => (
        <>
          <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={selectedTypeRequest}
            label="Age"
            onChange={(event) => {
              setSelectedTypeRequest(event.target.value);
            }}
          >
            {typeRequestOptions.map((x) => (
              <MenuItem value={x.value}>{x.label}</MenuItem>
            ))}
          </Select>
        </>
      ),
    },
    {
      field: "technical",
      headerName: "Técnico",
      width: 250,
      editable: true,
      renderEditCell: (params) => (
        <>
          <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={selectedTechnician}
            label="Age"
            onChange={(event) => {
              setSelectedTechnician(event.target.value);
            }}
          >
            {technicians.map((x) => (
              <MenuItem value={x.value}>{x.label}</MenuItem>
            ))}
          </Select>
        </>
      ),
    },
    {
      field: "hours_worked",
      headerName: "Horas trabajadas",
      width: 200,
      editable: true,
      renderEditCell: (params) => (
        <>
          <TextField
            id="standard-basic"
            label="Standard"
            variant="standard"
            onChange={(e) => setHoursWorked(e.target.value)}
            value={hoursWorked}
          />
        </>
      ),
    },
    {
      field: "actions",
      type: "actions",
      headerName: "OPCIONES",
      width: 218,
      cellClassName: "actions",
      getActions: ({ id }) => {
        const isInEditMode = rowModesModel[id]?.mode === "edit";

        if (isInEditMode) {
          return [
            <GridActionsCellItem
              icon={loading ? <CircularProgress /> : <SaveIcon />}
              label="Save"
              sx={{
                color: "primary.main",
              }}
              onClick={handleSaveClick(id)}
            />,
          ];
        }

        return [
          <GridActionsCellItem
            icon={loading ? <CircularProgress /> : <EditIcon />}
            label="Edit"
            className="textPrimary"
            onClick={handleEditClick(id)}
            color="inherit"
          />,
        ];
      },
    },
  ];

  return (
    <Box
      sx={{
        height: "calc(100vh - 64px)",
        width: "100%",
        "& .actions": {
          color: "text.secondary",
        },
        "& .textPrimary": {
          color: "text.primary",
        },
      }}
    >
      <DataGrid
        rows={rows}
        columns={columns}
        editMode="row"
        onRowModesModelChange={handleRowModesModelChange}
        onRowEditStop={handleRowEditStop}
        processRowUpdate={processRowUpdate}
        pagination
        rowCount={rows.length}
        onPageChange={(params) => setPage(params.page)}
        slotProps={{
          toolbar: { setRows, setRowModesModel },
        }}
      />
      {backdrop ? (
        <Backdrop
          sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1 }}
          open={backdrop}
        >
          <CircularProgress color="inherit" />
        </Backdrop>
      ) : null}
    </Box>
  );
}
