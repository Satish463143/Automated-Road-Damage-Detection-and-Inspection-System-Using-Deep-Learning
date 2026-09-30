import { Navigate, Route, Routes } from "react-router-dom";

import AppLayout from "./components/layout/AppLayout";
import Dashboard from "./pages/Dashboard";
import InspectRoad from "./pages/InspectRoad";
import InspectionHistory from "./pages/InspectionHistory";
import InspectionDetail from "./pages/InspectionDetail";
import ModelPerformance from "./pages/ModelPerformance";
import NotFound from "./pages/NotFound";

export default function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route index element={<Dashboard />} />
        <Route path="/inspect" element={<InspectRoad />} />
        <Route path="/inspections" element={<InspectionHistory />} />
        <Route path="/inspections/:inspectionId" element={<InspectionDetail />} />
        <Route path="/model" element={<ModelPerformance />} />
        <Route path="/dashboard" element={<Navigate to="/" replace />} />
      </Route>

      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}
