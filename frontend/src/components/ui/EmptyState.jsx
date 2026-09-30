export default function EmptyState({
  title = "No data yet",
  description,
  action,
}) {
  return (
    <div className="empty-state">
      <div className="empty-state-icon" aria-hidden="true">
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.6"
        >
          <path d="M4 6h16v12H4z" />
          <path d="M8 10h8M8 14h5" />
        </svg>
      </div>
      <h3>{title}</h3>
      {description && <p>{description}</p>}
      {action}
    </div>
  );
}
