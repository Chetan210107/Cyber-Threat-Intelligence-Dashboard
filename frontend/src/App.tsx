import { Navigate, Route, BrowserRouter, Routes } from "react-router-dom";
import type { ReactNode } from "react";

import { hasSession } from "./lib/session";
import DashboardLayout from "./components/layout/DashboardLayout";
import AuthPage from "./pages/AuthPage";
import CompleteProfilePage from "./pages/CompleteProfilePage";
import DashboardPage from "./pages/DashboardPage";
import ComingSoonPage from "./pages/ComingSoonPage";
import ProfilePage from "./pages/ProfilePage";
import VirusTotalPage from "./pages/VirusTotalPage";
import WelcomePage from "./pages/WelcomePage";

function RequireSession({ children }: { children: ReactNode }) {
  if (!hasSession()) {
    return <Navigate to="/" replace />;
  }
  return children;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AuthPage />} />
        <Route path="/welcome" element={<RequireSession><WelcomePage /></RequireSession>} />
        <Route path="/profile/complete" element={<RequireSession><CompleteProfilePage /></RequireSession>} />
        <Route
          element={
            <RequireSession>
              <DashboardLayout />
            </RequireSession>
          }
        >
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/virustotal" element={<VirusTotalPage />} />
          <Route path="/threat-intelligence" element={<ComingSoonPage title="Threat Intelligence" />} />
          <Route path="/ioc-search" element={<ComingSoonPage title="IOC Search" />} />
          <Route path="/malware-intelligence" element={<ComingSoonPage title="Malware Intelligence" />} />
          <Route path="/mitre-attck" element={<ComingSoonPage title="MITRE ATT&CK" />} />
          <Route path="/reports" element={<ComingSoonPage title="Reports" />} />
          <Route path="/settings" element={<ComingSoonPage title="Settings" />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
