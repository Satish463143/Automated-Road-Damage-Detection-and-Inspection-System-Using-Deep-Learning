export default function DamageBadge({ code, name }) {
  return (
    <span className={`damage-badge damage-${code || "unknown"}`}>
      <span>{code || "N/A"}</span>
      <strong>{name || "Unknown"}</strong>
    </span>
  );
}
