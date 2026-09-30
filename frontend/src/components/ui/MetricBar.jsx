import { clamp, formatPercent } from "../../utils/format";

export default function MetricBar({ label, value }) {
  const percent = clamp(value) * 100;

  return (
    <div className="metric-bar-block">
      <div className="metric-bar-label">
        <span>{label}</span>
        <strong>{formatPercent(value)}</strong>
      </div>

      <div className="metric-bar-track">
        <div
          className="metric-bar-fill"
          style={{ width: `${percent}%` }}
        />
      </div>
    </div>
  );
}
