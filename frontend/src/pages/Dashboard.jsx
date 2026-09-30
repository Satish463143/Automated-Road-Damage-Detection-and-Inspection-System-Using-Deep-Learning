import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import DamageDistribution from "../components/dashboard/DamageDistribution";
import EmptyState from "../components/ui/EmptyState";
import ErrorState from "../components/ui/ErrorState";
import LoadingState from "../components/ui/LoadingState";
import PageHeader from "../components/ui/PageHeader";
import StatCard from "../components/ui/StatCard";
import StatusBadge from "../components/ui/StatusBadge";
import { DAMAGE_CLASSES } from "../data/damageClasses";
import { api } from "../services/api";
import {
  formatDateTime,
  formatNumber,
  formatPercent,
} from "../utils/format";

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [recent, setRecent] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadDashboard() {
    setLoading(true);
    setError("");

    try {
      const [analytics, inspections] = await Promise.all([
        api.getAnalyticsSummary(),
        api.listInspections({ limit: 5, offset: 0 }),
      ]);

      setSummary(analytics);
      setRecent(inspections.items || []);
    } catch (err) {
      setError(err.message || "Failed to load dashboard.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  if (loading) {
    return <LoadingState message="Loading dashboard..." />;
  }

  if (error) {
    return (
      <ErrorState
        title="Dashboard unavailable"
        message={error}
        action={
          <button className="button button-primary" onClick={loadDashboard}>
            Try again
          </button>
        }
      />
    );
  }

  const distribution = summary?.damage_distribution || [];
  const byCode = Object.fromEntries(
    distribution.map((item) => [item.damage_code, item.count])
  );

  return (
    <div className="page-stack">
      <PageHeader
        eyebrow="System overview"
        title="Road Damage Dashboard"
        description="Review inspections, detected road damage, and model activity."
        actions={
          <Link to="/inspect" className="button button-primary">
            New inspection
          </Link>
        }
      />

      <div className="stats-grid">
        <StatCard
          label="Inspections"
          value={formatNumber(summary?.total_inspections)}
          helper={`${formatNumber(summary?.completed_inspections)} completed`}
        />
        <StatCard
          label="Detections"
          value={formatNumber(summary?.total_detections)}
          helper={`Avg. confidence ${formatPercent(summary?.average_confidence)}`}
        />
        <StatCard
          label="Potholes"
          code="D40"
          value={formatNumber(byCode.D40 || 0)}
          helper={DAMAGE_CLASSES.D40.name}
        />
        <StatCard
          label="Alligator cracks"
          code="D20"
          value={formatNumber(byCode.D20 || 0)}
          helper={DAMAGE_CLASSES.D20.name}
        />
      </div>

      <div className="dashboard-grid">
        <section className="card">
          <div className="section-heading">
            <div>
              <span>Analytics</span>
              <h2>Damage distribution</h2>
            </div>
          </div>

          <DamageDistribution items={distribution} />
        </section>

        <section className="card">
          <div className="section-heading">
            <div>
              <span>System status</span>
              <h2>Inspection completion</h2>
            </div>
          </div>

          <div className="completion-block">
            <div className="completion-number">
              {formatNumber(summary?.completed_inspections)}
            </div>
            <p>Completed inspections</p>

            <div className="completion-meta">
              <div>
                <span>Failed</span>
                <strong>{formatNumber(summary?.failed_inspections)}</strong>
              </div>
              <div>
                <span>Total</span>
                <strong>{formatNumber(summary?.total_inspections)}</strong>
              </div>
            </div>
          </div>
        </section>
      </div>

      <section className="card">
        <div className="section-heading section-heading-row">
          <div>
            <span>Latest activity</span>
            <h2>Recent inspections</h2>
          </div>

          <Link to="/inspections" className="text-link">
            View all
          </Link>
        </div>

        {!recent.length ? (
          <EmptyState
            title="No inspections yet"
            description="Upload your first road image to create an inspection."
            action={
              <Link to="/inspect" className="button button-primary">
                Inspect road
              </Link>
            }
          />
        ) : (
          <div className="table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Image</th>
                  <th>Status</th>
                  <th>Detections</th>
                  <th>Confidence</th>
                  <th>Date</th>
                  <th />
                </tr>
              </thead>

              <tbody>
                {recent.map((item) => (
                  <tr key={item.id}>
                    <td>
                      <div className="file-cell">
                        <span className="file-icon">IMG</span>
                        <div>
                          <strong>{item.original_filename}</strong>
                          <small>
                            {item.image_width} × {item.image_height}
                          </small>
                        </div>
                      </div>
                    </td>
                    <td>
                      <StatusBadge status={item.status} />
                    </td>
                    <td>{item.total_detections}</td>
                    <td>{formatPercent(item.average_confidence)}</td>
                    <td>{formatDateTime(item.created_at)}</td>
                    <td>
                      <Link
                        className="table-action"
                        to={`/inspections/${item.id}`}
                      >
                        View
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
}
