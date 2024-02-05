import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
  Router,
  Switch,
} from "react-router-dom";
import { ListOfTechnicians } from "./pages/ListOfTechnicians";
import { TechniciansReport } from "./pages/TechniciansReport";
import { ListOrders } from "./pages/ListOrders";
import ButtonAppBar from "./components/NavBar";

function App() {
  return (
    <BrowserRouter>
      <ButtonAppBar />
      <Routes>
        <Route path="/list-technicians" element={<ListOfTechnicians />} />
        <Route path="/technicians-report" element={<TechniciansReport />} />
        <Route path="/list-orders" element={<ListOrders />} />
        <Route path="/" element={<Navigate to="/list-technicians" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
