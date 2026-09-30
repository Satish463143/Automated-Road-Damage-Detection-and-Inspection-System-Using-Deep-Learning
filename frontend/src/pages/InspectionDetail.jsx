import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

import DetectionTable from "../components/inspection/DetectionTable";
import ImageComparison from "../components/inspection/ImageComparison";
import InspectionSummary from "../components/inspection/InspectionSummary";
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

export default function InspectionDetail() {
  const { inspectionId } = useParams();
  const navigate = useNavigate();

  const [inspection, setInspection] = useState(null);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState("");

  async function loadInspection() {
    setLoading(true);
    setError("");

    try {
      const result = await api.getInspection(inspectionId);
      setInspection(result);
    } catch (err) {
      setError(err.message || "Failed to load inspection.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadInspection();
  }, [inspectionId]);

  async function deleteInspection() {
    const confirmed = window.confirm(
      "Delete this inspection and its stored images?"
    );

    if (!confirmed) return;

    setDeleting(true);

    try {
      await api.deleteInspection(inspectionId);
      navigate("/inspections");
    } catch (err) {
      setError(err.message || "Failed to delete inspection.");
      setDeleting(false);
    }
  }

  if (loading) {
    return <LoadingState message="Loading inspection..." />;
  }

  if (error || !inspection) {
    return (
      <ErrorState
        title="Inspection unavailable"
        message={error || "Inspection was not found."}
        action={
          <Link to="/inspections" className="button button-secondary">
            Back to history
          </Link>
        }
      />
    );
  }

  return (
    <div className="page-stack">
      <PageHeader
        eyebrow="Inspection record"
        title={inspection.original_filename}
        description={`Created ${formatDateTime(inspection.created_at)}`}
        actions={
          <>
            <Link to="/inspections" className="button button-secondary">
              Back
            </Link>
            <button
              type="button"
              className="button button-danger"
              onClick={deleteInspection}
              disabled={deleting}
            >
              {deleting ? "Deleting..." : "Delete"}
            </button>
          </>
        }
      />

      <section className="card inspection-meta-card">
        <div className="inspection-meta">
          <div>
            <span>Status</span>
            <StatusBadge status={inspection.status} />
          </div>
          <div>
            <span>Model</span>
            <strong>{inspection.model_version || "N/A"}</strong>
          </div>
          <div>
            <span>Image size</span>
            <strong>
              {inspection.image_width} × {inspection.image_height}
            </strong>
          </div>
          <div>
            <span>Confidence</span>
            <strong>{formatPercent(inspection.average_confidence)}</strong>
          </div>
          <div>
            <span>Processing time</span>
            <strong>{formatMilliseconds(inspection.processing_time_ms)}</strong>
          </div>
        </div>
      </section>

      <InspectionSummary inspection={inspection} />

      <ImageComparison
        originalUrl={inspection.original_image_url}
        resultUrl={inspection.result_image_url}
      />

      <section className="card">
        <div className="section-heading">
          <div>
            <span>Model output</span>
            <h2>Detection records</h2>
          </div>
        </div>

        <DetectionTable detections={inspection.detections} />
      </section>
    </div>
  );
}
