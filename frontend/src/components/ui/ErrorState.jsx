export default function ErrorState({
  title = "Something went wrong",
  message,
  action,
}) {
  return (
    <div className="error-state">
      <strong>{title}</strong>
      <p>{message || "The request failed."}</p>
      {action}
    </div>
  );
}
