import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <main className="not-found">
      <div className="not-found-card">
        <span>404</span>
        <h1>Page not found</h1>
        <p>The page you requested does not exist.</p>
        <Link to="/" className="button button-primary">
          Go to dashboard
        </Link>
      </div>
    </main>
  );
}
