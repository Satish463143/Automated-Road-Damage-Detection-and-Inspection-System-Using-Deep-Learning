import { useApiStatus } from "../../hooks/useApiStatus";

export default function ApiStatus() {
  const { backend, database, model, loading, refresh } = useApiStatus();

  const backendHealthy =
    backend === "healthy" || backend === "degraded";

  return (
    <button
      type="button"
      className="api-status"
      onClick={refresh}
      title={`Backend: ${backend}, Database: ${database}, Model: ${model}`}
    >
      <span
        className={`status-dot ${
          loading
            ? "status-dot-neutral"
            : backendHealthy
              ? "status-dot-success"
              : "status-dot-danger"
        }`}
      />
      <span className="api-status-copy">
        <strong>{loading ? "Checking API" : backendHealthy ? "API Online" : "API Offline"}</strong>
        <small>
          DB {database} · Model {model}
        </small>
      </span>
    </button>
  );
}
