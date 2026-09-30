import { NavLink } from "react-router-dom";

import { APP_NAME } from "../../config/appConfig";

const NAV_ITEMS = [
  { to: "/", label: "Dashboard", icon: "grid", end: true },
  { to: "/inspect", label: "Inspect Road", icon: "scan" },
  { to: "/inspections", label: "Inspection History", icon: "history" },
  { to: "/model", label: "Model Performance", icon: "model" },
];

function NavIcon({ name }) {
  const paths = {
    grid: (
      <>
        <rect x="3" y="3" width="7" height="7" rx="1" />
        <rect x="14" y="3" width="7" height="7" rx="1" />
        <rect x="3" y="14" width="7" height="7" rx="1" />
        <rect x="14" y="14" width="7" height="7" rx="1" />
      </>
    ),
    scan: (
      <>
        <path d="M4 8V5a1 1 0 0 1 1-1h3" />
        <path d="M16 4h3a1 1 0 0 1 1 1v3" />
        <path d="M20 16v3a1 1 0 0 1-1 1h-3" />
        <path d="M8 20H5a1 1 0 0 1-1-1v-3" />
        <path d="M7 12h10" />
      </>
    ),
    history: (
      <>
        <path d="M3 12a9 9 0 1 0 3-6.7L3 8" />
        <path d="M3 3v5h5" />
        <path d="M12 7v5l3 2" />
      </>
    ),
    model: (
      <>
        <rect x="4" y="4" width="16" height="16" rx="3" />
        <path d="M9 9h6v6H9z" />
        <path d="M9 1v3M15 1v3M9 20v3M15 20v3" />
        <path d="M1 9h3M1 15h3M20 9h3M20 15h3" />
      </>
    ),
  };

  return (
    <svg
      className="nav-icon"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      {paths[name]}
    </svg>
  );
}

export default function Sidebar({ open, onClose }) {
  return (
    <aside className={`sidebar ${open ? "sidebar-open" : ""}`}>
      <div className="sidebar-brand">
        <div className="brand-mark" aria-hidden="true">
          RD
        </div>
        <div>
          <div className="brand-title">{APP_NAME}</div>
          <div className="brand-subtitle">DS-ML Project</div>
        </div>
      </div>

      <nav className="sidebar-nav" aria-label="Main navigation">
        {NAV_ITEMS.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.end}
            onClick={onClose}
            className={({ isActive }) =>
              `nav-link ${isActive ? "nav-link-active" : ""}`
            }
          >
            <NavIcon name={item.icon} />
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div className="sidebar-class-list">
          <span>D00</span>
          <span>D10</span>
          <span>D20</span>
          <span>D40</span>
        </div>
        <p>Road surface damage detection</p>
      </div>
    </aside>
  );
}
