export default function PageHeader({
  eyebrow,
  title,
  description,
  actions,
}) {
  return (
    <div className="page-header">
      <div>
        {eyebrow && <div className="page-eyebrow">{eyebrow}</div>}
        <h1>{title}</h1>
        {description && <p>{description}</p>}
      </div>

      {actions && <div className="page-actions">{actions}</div>}
    </div>
  );
}
