import { useState } from "react";
import { Outlet } from "react-router-dom";

import Header from "./Header";
import Sidebar from "./Sidebar";

export default function AppLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="app-shell">
      <Sidebar
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      <div className="app-main">
        <Header
          onMenuClick={() => setSidebarOpen((current) => !current)}
        />

        <main className="page-container">
          <Outlet />
        </main>
      </div>

      {sidebarOpen && (
        <button
          type="button"
          className="sidebar-overlay"
          aria-label="Close navigation"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  );
}
