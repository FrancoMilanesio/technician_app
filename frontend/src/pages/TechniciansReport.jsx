import { useEffect, useState } from "react";
import * as React from "react";
import { getTechniciansReport } from "../api/TechniciansReport.api";
import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Pagination from "@mui/material/Pagination";
import Stack from "@mui/material/Stack";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import Divider from "@mui/material/Divider";
import ListItemText from "@mui/material/ListItemText";
import ListItemAvatar from "@mui/material/ListItemAvatar";
import Avatar from "@mui/material/Avatar";
import TextField from "@mui/material/TextField";

export function TechniciansReport() {
  const [techniciansReport, setTechniciansReport] = useState([]);

  useEffect(() => {
    const fetchTechniciansReport = async () => {
      const techniciansReportData = await getTechniciansReport();
      setTechniciansReport(techniciansReportData.data);
    };

    fetchTechniciansReport();
  }, []);

  const bull = (
    <Box
      component="span"
      sx={{ display: "inline-block", mx: "2px", transform: "scale(0.8)" }}
    >
      •
    </Box>
  );

  return (
    <Card sx={{ minWidth: 275 }}>
      <CardContent>
        <Typography variant="h6" color="text.primary" gutterBottom>
          Promedio cobrado general por técnico:
        </Typography>
        <Typography variant="h5" component="div" color="text.secondary">
          ${techniciansReport.average_amount}
        </Typography>
      </CardContent>

      <CardContent>
        <Typography variant="h6" color="text.primary" gutterBottom>
          Técnicos que cobran menos que el promedio:
        </Typography>
        <List>
          {techniciansReport.less_than_average &&
            techniciansReport.less_than_average.map((technical, index) => (
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
                          {` - ${technical.total_hours_worked}hs - $${technical.hours_worked_total_amount}`}
                        </Typography>
                      </React.Fragment>
                    }
                  />
                </ListItem>
                <Divider variant="inset" component="li" />
              </React.Fragment>
            ))}
        </List>
      </CardContent>

      <CardContent>
        <Typography variant="h6" color="text.primary" gutterBottom>
          Último trabajador ingresado que cobró el monto más bajo:
        </Typography>
        <List>
          {techniciansReport.lowest_amount && (
            <ListItem alignItems="flex-start">
              <ListItemAvatar>
                <Avatar
                  alt={techniciansReport.lowest_amount.full_name}
                  src={`/static/images/avatar/lowest.jpg`}
                />
              </ListItemAvatar>
              <ListItemText
                primary={techniciansReport.lowest_amount.full_name}
                secondary={
                  <React.Fragment>
                    <Typography
                      sx={{ display: "inline" }}
                      component="span"
                      variant="body2"
                      color="text.primary"
                    >
                      {` - ${techniciansReport.lowest_amount.total_hours_worked}hs - $${techniciansReport.lowest_amount.hours_worked_total_amount}`}
                    </Typography>
                  </React.Fragment>
                }
              />
            </ListItem>
          )}
        </List>
      </CardContent>

      <CardContent>
        <Typography variant="h6" color="text.primary" gutterBottom>
          Último trabajador ingresado que cobró el monto más alto:
        </Typography>
        <List>
          {techniciansReport.highest_amount && (
            <ListItem alignItems="flex-start">
              <ListItemAvatar>
                <Avatar
                  alt={techniciansReport.highest_amount.full_name}
                  src={`/static/images/avatar/highest.jpg`}
                />
              </ListItemAvatar>
              <ListItemText
                primary={techniciansReport.highest_amount.full_name}
                secondary={
                  <React.Fragment>
                    <Typography
                      sx={{ display: "inline" }}
                      component="span"
                      variant="body2"
                      color="text.primary"
                    >
                      {` - ${techniciansReport.highest_amount.total_hours_worked}hs - $${techniciansReport.highest_amount.hours_worked_total_amount}`}
                    </Typography>
                  </React.Fragment>
                }
              />
            </ListItem>
          )}
        </List>
      </CardContent>
    </Card>
  );
}
