export default function DashboardPage() {
  return (
    <section className="content-panel dashboard-home-panel">
      <div className="eyebrow">CTID Dashboard</div>
      <h2 className="section-title">Welcome back, analyst.</h2>
      <p className="section-copy">
        The dashboard shell is ready. This is the main landing surface for future CTID intelligence widgets, charts, and
        reports.
      </p>

      <div className="dashboard-kpi-grid">
        <div className="dashboard-kpi-card">
          <span className="kpi-label">Open Cases</span>
          <strong className="kpi-value">12</strong>
        </div>
        <div className="dashboard-kpi-card">
          <span className="kpi-label">Active Feeds</span>
          <strong className="kpi-value">8</strong>
        </div>
        <div className="dashboard-kpi-card">
          <span className="kpi-label">Pending Alerts</span>
          <strong className="kpi-value">24</strong>
        </div>
      </div>
    </section>
  );
}
