import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";

import DetectionTable from "../components/inspection/DetectionTable";
import ImageComparison from "../components/inspection/ImageComparison";
import InspectionSummary from "../components/inspection/InspectionSummary";
import ErrorState from "../components/ui/ErrorState";
import PageHeader from "../components/ui/PageHeader";
import { MAX_UPLOAD_SIZE_MB } from "../config/appConfig";
import { api } from "../services/api";
import { validateRoadImage } from "../utils/fileValidation";

export default function InspectRoad() {
  const inputRef = useRef(null);

  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [dragging, setDragging] = useState(false);
  const [inspection, setInspection] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!file) {
      setPreviewUrl("");
      return undefined;
    }

    const url = URL.createObjectURL(file);
    setPreviewUrl(url);

    return () => URL.revokeObjectURL(url);
  }, [file]);

  function chooseFile(nextFile) {
    setError("");
    setInspection(null);

    const validationError = validateRoadImage(nextFile);

    if (validationError) {
      setFile(null);
      setError(validationError);
      return;
    }

    setFile(nextFile);
  }

  function onInputChange(event) {
    chooseFile(event.target.files?.[0] || null);
  }

  function onDrop(event) {
    event.preventDefault();
    setDragging(false);
    chooseFile(event.dataTransfer.files?.[0] || null);
  }

  async function analyze() {
    if (!file) {
      setError("Choose a road image first.");
      return;
    }

    setSubmitting(true);
    setError("");
    setInspection(null);

    try {
      const result = await api.createInspection(file);
      setInspection(result);
    } catch (err) {
      setError(err.message || "Road inspection failed.");
    } finally {
      setSubmitting(false);
    }
  }

  function reset() {
    setFile(null);
    setInspection(null);
    setError("");
    if (inputRef.current) {
      inputRef.current.value = "";
    }
  }

  return (
    <div className="page-stack">
      <PageHeader
        eyebrow="Image analysis"
        title="Inspect Road Image"
        description="Upload a JPG or PNG road image and run the trained road damage detector."
      />

      <section className="card upload-card">
        <div
          className={`drop-zone ${dragging ? "drop-zone-active" : ""}`}
          onDragOver={(event) => {
            event.preventDefault();
            setDragging(true);
          }}
          onDragLeave={() => setDragging(false)}
          onDrop={onDrop}
        >
          <input
            ref={inputRef}
            className="sr-only"
            type="file"
            accept="image/jpeg,image/png"
            onChange={onInputChange}
          />

          {!previewUrl ? (
            <>
              <div className="upload-icon" aria-hidden="true">
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="1.6"
                >
                  <path d="M12 16V4" />
                  <path d="m7 9 5-5 5 5" />
                  <path d="M5 14v5h14v-5" />
                </svg>
              </div>

              <h2>Upload road image</h2>
              <p>
                Drop a road photograph here or choose a file from your computer.
              </p>

              <button
                type="button"
                className="button button-secondary"
                onClick={() => inputRef.current?.click()}
              >
                Choose image
              </button>

              <small>JPG or PNG · Maximum {MAX_UPLOAD_SIZE_MB} MB</small>
            </>
          ) : (
            <div className="selected-upload">
              <img src={previewUrl} alt="Selected road" />

              <div className="selected-upload-copy">
                <span>Ready for inspection</span>
                <h2>{file.name}</h2>
                <p>{(file.size / 1024 / 1024).toFixed(2)} MB</p>

                <div className="button-row">
                  <button
                    type="button"
                    className="button button-secondary"
                    onClick={() => inputRef.current?.click()}
                    disabled={submitting}
                  >
                    Change image
                  </button>

                  <button
                    type="button"
                    className="button button-primary"
                    onClick={analyze}
                    disabled={submitting}
                  >
                    {submitting ? "Analyzing..." : "Analyze road"}
                  </button>

                  <button
                    type="button"
                    className="button button-ghost"
                    onClick={reset}
                    disabled={submitting}
                  >
                    Clear
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </section>

      {submitting && (
        <section className="analysis-progress card">
          <div className="spinner" />
          <div>
            <strong>Running road damage detection</strong>
            <p>
              The backend is processing the image with the trained model.
            </p>
          </div>
        </section>
      )}

      {error && (
        <ErrorState
          title="Inspection failed"
          message={error}
        />
      )}

      {inspection && (
        <>
          <section className="result-banner">
            <div>
              <span>Inspection complete</span>
              <h2>
                {inspection.total_detections === 0
                  ? "No road damage detected"
                  : `${inspection.total_detections} damage ${
                      inspection.total_detections === 1
                        ? "instance"
                        : "instances"
                    } detected`}
              </h2>
            </div>

            <Link
              className="button button-secondary"
              to={`/inspections/${inspection.id}`}
            >
              Open full record
            </Link>
          </section>

          <InspectionSummary inspection={inspection} />

          <ImageComparison
            originalUrl={inspection.original_image_url}
            resultUrl={inspection.result_image_url}
          />

          <section className="card">
            <div className="section-heading">
              <div>
                <span>Detection output</span>
                <h2>Detected road damage</h2>
              </div>
            </div>

            <DetectionTable detections={inspection.detections} />
          </section>
        </>
      )}
    </div>
  );
}
