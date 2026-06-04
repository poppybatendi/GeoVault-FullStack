import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import MapView from "./pages/MapView";
import Samples from "./pages/Samples";
import AIInsights from "./pages/AIInsights";
import Reports from "./pages/Reports";

function App() {
  return (
    <BrowserRouter>

      <Routes>

        <Route
          path="/"
          element={<Login />}
        />

        <Route
          path="/dashboard"
          element={<Dashboard />}
        />

        <Route
          path="/map"
          element={<MapView />}
        />

        <Route
          path="/samples"
          element={<Samples />}
        />

        <Route
          path="/ai"
          element={<AIInsights />}
        />

        <Route
          path="/ai"
          element={<AIInsights />}
        />

        <Route
          path="/reports"
          element={<Reports />}
        />

      </Routes>

    </BrowserRouter>
  );
}

export default App;