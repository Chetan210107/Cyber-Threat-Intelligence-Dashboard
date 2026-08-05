type ComingSoonPageProps = {
  title: string;
};

export default function ComingSoonPage({ title }: ComingSoonPageProps) {
  return (
    <section className="content-panel coming-soon-panel">
      <div className="eyebrow">{title}</div>
      <h2 className="section-title">Coming Soon</h2>
      <p className="section-copy">
        This section is reserved for a future CTID module. The dashboard layout is in place, and this page will be
        expanded later without changing the navigation shell.
      </p>
    </section>
  );
}
