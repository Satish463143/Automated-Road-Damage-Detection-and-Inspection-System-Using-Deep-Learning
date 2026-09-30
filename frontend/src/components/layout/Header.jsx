import ApiStatus from "../ui/ApiStatus";

export default function Header({ onMenuClick }) {
  return (
    <header className="topbar">
      <button
        type="button"
        className="menu-button"
        onClick={onMenuClick}
        aria-label="Open navigation"
      >
        <span />
        <span />
        <span />
      </button>

      <div className="topbar-copy">
        <span className="topbar-eyebrow">Automated road inspection</span>
        <strong>Image Detection Dashboard</strong>
      </div>

      <ApiStatus />
    </header>
  );
}
