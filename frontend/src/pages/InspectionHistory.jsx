import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import EmptyState from "../components/ui/EmptyState";
import ErrorState from "../components/ui/ErrorState";
import LoadingState from "../components/ui/LoadingState";
import PageHeader from "../components/ui/PageHeader";
import StatusBadge from "../components/ui/StatusBadge";
import { api } from "../services/api";
import {
  formatDateTime,
  formatMilliseconds,
  formatPercent,
} from "../utils/format";

const PAGE_SIZE = 20;

export default function InspectionHistory() {
  const [data, setData] = useState({
    items: [],
    total: 0,
    limit: PAGE_SIZE,
    offset: 0,
  });
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [deletingId, setDeletingId] = useState("");
  const [error, setError] = useState("");

  async function load(targetPage = page) {
    setLoading(true);
    setError("");

    try {
      const offset = (targetPage - 1) * PAGE_SIZE;
      const result = await api.listInspections({
        limit: PAGE_SIZE,
        offset,
      });

      setData(result);
    } catch (err) {
      setError(err.message || "Failed to load inspection history.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load(page);
  }, [page]);

  async function removeInspection(id) {
    const confirmed = window.confirm(
      "Delete this inspection and its stored images?"
    );

    if (!confirmed) return;

    setDeletingId(id);

    try {
      await api.deleteInspection(id);

      const remainingOnPage = data.items.length - 1;
      if (remainingOnPage === 0 && page > 1) {
        setPage((current) => current - 1);
      } else {
        await load(page);
      }
    } catch (err) {
      setError(err.message || "Failed to delete inspection.");
    } finally {
      setDeletingId("");
    }
  }

  if (loading && !data.items.length) {
    return <LoadingState message="Loading inspection history..." />;
  }

  const totalPages = Math.max(1, Math.ceil(data.total / PAGE_SIZE));

  return (
    <div className="page-stack">
      <PageHeader
        eyebrow="Inspection records"
        title="Inspection History"
        description="Review every uploaded road image and its detection result."
        actions={
          <Link to="/inspect" className="button button-primary">
            New inspection
          </Link>
        }
      />

      {error && (
        <ErrorState
          title="History unavailable"
          message={error}
          action={
            <button className="button button-secondary" onClick={() => load(page)}>
              Retry
            </button>
          }
        />
      )}

      <section className="card">
        {!data.items.length && !loading ? (
          <EmptyState
            title="No inspections found"
            description="Your completed road image inspections will appear here."
            action={
              <Link to="/inspect" className="button button-primary">
                Inspect first image
              </Link>
            }
          />
        ) : (
          <>
            <div className="section-heading section-heading-row">
              <div>
                <span>Database records</span>
                <h2>{data.total} inspections</h2>
              </div>

              {loading && <span className="subtle-text">Refreshing...</span>}
            </div>

            <div className="table-wrap">
              <table className="data-table history-table">
                <thead>
                  <tr>
                    <th>Image</th>
                    <th>Status</th>
                    <th>Damage</th>
                    <th>Confidence</th>
                    <th>Processing</th>
                    <th>Date</th>
                    <th />
                  </tr>
                </thead>

                <tbody>
                  {data.items.map((item) => (
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
                      <td>{formatMilliseconds(item.processing_time_ms)}</td>
                      <td>{formatDateTime(item.created_at)}</td>
                      <td>
                        <div className="row-actions">
                          <Link
                            to={`/inspections/${item.id}`}
                            className="table-action"
                          >
                            View
                          </Link>
                          <button
                            type="button"
                            className="table-action table-action-danger"
                            disabled={deletingId === item.id}
                            onClick={() => removeInspection(item.id)}
                          >
                            {deletingId === item.id ? "Deleting" : "Delete"}
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="pagination">
              <button
                type="button"
                className="button button-secondary button-small"
                disabled={page <= 1 || loading}
                onClick={() => setPage((current) => current - 1)}
              >
                Previous
              </button>

              <span>
                Page {page} of {totalPages}
              </span>

              <button
                type="button"
                className="button button-secondary button-small"
                disabled={page >= totalPages || loading}
                onClick={() => setPage((current) => current + 1)}
              >
                Next
              </button>
            </div>
          </>
        )}
      </section>
    </div>
  );
}
