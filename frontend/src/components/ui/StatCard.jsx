export default function StatCard({
  label,
  value,
  helper,
  code,
}) {
  return (
    <article className="stat-card">
      <div className="stat-card-top">
        <span>{label}</span>
        {code && <span className="stat-code">{code}</span>}
      </div>
      <strong className="stat-value">{value}</strong>
      {helper && <small>{helper}</small>}
    </article>
  );
}
