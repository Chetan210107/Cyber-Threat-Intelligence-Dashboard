export type DashboardNavItem = {
  label: string;
  path: string;
  comingSoon?: boolean;
};

export const dashboardNavigation: DashboardNavItem[] = [
  { label: "Dashboard", path: "/dashboard" },
  { label: "Threat Intelligence", path: "/threat-intelligence", comingSoon: true },
  { label: "IOC Search", path: "/ioc-search", comingSoon: true },
  { label: "Malware Intelligence", path: "/malware-intelligence", comingSoon: true },
  { label: "MITRE ATT&CK", path: "/mitre-attck", comingSoon: true },
  { label: "Reports", path: "/reports", comingSoon: true },
  { label: "Profile", path: "/profile" },
  { label: "Settings", path: "/settings", comingSoon: true },
];
