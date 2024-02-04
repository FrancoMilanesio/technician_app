import { Link } from 'react-router-dom';
import Box from '@mui/material/Box';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Button from '@mui/material/Button';

export default function ButtonAppBar() {
    return (
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <Button color="inherit">
              <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
                Home
              </Link>
            </Button>
            <Box sx={{ marginLeft: 'auto' }}>
              <Button color="inherit">
                <Link to="/list-technicians" style={{ textDecoration: 'none', color: 'inherit' }}>
                  List of Technicians
                </Link>
              </Button>
              <Button color="inherit">
                <Link to="/technicians-report" style={{ textDecoration: 'none', color: 'inherit' }}>
                  Technicians Report
                </Link>
              </Button>
            </Box>
          </Toolbar>
        </AppBar>
      </Box>
    );
  }