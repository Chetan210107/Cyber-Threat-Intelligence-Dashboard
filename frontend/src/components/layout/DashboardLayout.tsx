import { useMemo, useState } from "react";
import { NavLink, Outlet, useLocation, useNavigate } from "react-router-dom";

import { clearSession } from "../../lib/session";
import { dashboardNavigation } from "../../data/dashboardNavigation";

const routeTitles: Record<string, string> = {
  "/dashboard": "Dashboard",
  "/profile": "Profile",
  "/virustotal": "VirusTotal",
  "/threat-intelligence": "Threat Intelligence",
  "/ioc-search": "IOC Search",
  "/malware-intelligence": "Malware Intelligence",
  "/mitre-attck": "MITRE ATT&CK",
  "/reports": "Reports",
  "/settings": "Settings",
};

export default function DashboardLayout() {
  const navigate = useNavigate();
  const location = useLocation();
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [isMobileOpen, setIsMobileOpen] = useState(false);

  const activeTitle = useMemo(() => routeTitles[location.pathname] ?? "Dashboard", [location.pathname]);

  function handleLogout() {
    clearSession();
    navigate("/");
  }

  return (
    <div className={`dashboard-shell ${isCollapsed ? "is-collapsed" : ""} ${isMobileOpen ? "is-mobile-open" : ""}`}>
      {isMobileOpen ? <button type="button" className="sidebar-backdrop" aria-label="Close navigation" onClick={() => setIsMobileOpen(false)} /> : null}
      <aside className="sidebar-panel">
        <div className="sidebar-header">
          <div className="logo-mark sidebar-logo">CTID</div>
          <button
            type="button"
            className="icon-button sidebar-toggle-desktop"
            onClick={() => setIsCollapsed((current) => !current)}
            aria-label="Toggle sidebar"
          >
            {isCollapsed ? "→" : "←"}
          </button>
          <button
            type="button"
            className="icon-button sidebar-toggle-mobile"
            onClick={() => setIsMobileOpen((current) => !current)}
            aria-label="Toggle mobile sidebar"
          >
            ☰
          </button>
        </div>

        <nav className="sidebar-nav" aria-label="Main dashboard navigation">
          {dashboardNavigation.map((item) => (
            <NavLink key={item.path} to={item.path} className={({ isActive }) => `sidebar-link ${isActive ? "is-active" : ""}`} onClick={() => setIsMobileOpen(false)}>
              <span className="sidebar-link-indicator" />
              <span className="sidebar-link-label">{item.label}</span>
              {item.comingSoon ? <span className="sidebar-badge">Soon</span> : null}
            </NavLink>
          ))}
          <button type="button" className="sidebar-link sidebar-logout" onClick={handleLogout}>
            <span className="sidebar-link-indicator" />
            <span className="sidebar-link-label">Logout</span>
          </button>
        </nav>
      </aside>

      <div className="dashboard-content-area">
        <header className="topbar-panel">
          <div className="topbar-left">
            <button type="button" className="icon-button topbar-mobile-toggle" onClick={() => setIsMobileOpen((current) => !current)} aria-label="Open navigation">
              ☰
            </button>
            <div>
              <div className="topbar-eyebrow">Cyber Threat Intelligence Dashboard</div>
              <h1 className="topbar-title">{activeTitle}</h1>
            </div>
          </div>

          <div className="topbar-actions">
            <div className="topbar-search">
              <span className="topbar-search-icon">⌕</span>
              <input type="text" placeholder="Search CTID" aria-label="Search CTID" disabled />
            </div>
            <div className="topbar-profile-chip">
              <span className="topbar-avatar">D</span>
              <div>
                <div className="topbar-profile-name">Demo Analyst</div>
                <div className="topbar-profile-role">Analyst</div>
              </div>
            </div>
          </div>
        </header>

        <main className="dashboard-main">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
