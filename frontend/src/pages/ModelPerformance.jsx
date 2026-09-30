import { useEffect, useState } from "react";

import ErrorState from "../components/ui/ErrorState";
import LoadingState from "../components/ui/LoadingState";
import MetricBar from "../components/ui/MetricBar";
import PageHeader from "../components/ui/PageHeader";
import StatCard from "../components/ui/StatCard";
import { api } from "../services/api";
import {
  formatDateTime,
  formatPercent,
} from "../utils/format";

export default function ModelPerformance() {
  const [model, setModel] = useState(null);
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function load() {
    setLoading(true);
    setError("");

    try {
      const [modelData, healthData] = await Promise.all([
        api.getModelInfo(),
        api.health(),
      ]);

      setModel(modelData);
      setHealth(healthData);
    } catch (err) {
      setError(err.message || "Failed to load model information.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  if (loading) {
    return <LoadingState message="Loading model information..." />;
  }

  if (error) {
    return (
      <ErrorState
        title="Model information unavailable"
        message={error}
        action={
          <button className="button button-secondary" onClick={load}>
            Retry
          </button>
        }
      />
    );
  }

  const hasMetrics =
    model.precision !== null ||
    model.recall !== null ||
    model.map50 !== null ||
    model.map50_95 !== null;

  return (
    <div className="page-stack">
      <PageHeader
        eyebrow="Machine learning"
        title="Model Performance"
        description="Track the model version, dataset, classes, and evaluation metrics used by the application."
      />

      <div className="stats-grid">
        <StatCard
          label="Model version"
          value={model.version}
          helper={model.architecture}
        />
        <StatCard
          label="Input size"
          value={`${model.image_size}px`}
          helper="Training and inference image size"
        />
        <StatCard
          label="Classes"
          value={model.classes?.length || 0}
          helper="Road damage categories"
        />
        <StatCard
          label="Runtime"
          value={health?.model === "loaded" ? "Loaded" : "Unavailable"}
          helper={`Database ${health?.database || "unknown"}`}
        />
      </div>

      <div className="dashboard-grid">
        <section className="card">
          <div className="section-heading">
            <div>
              <span>Configuration</span>
              <h2>Model details</h2>
            </div>
          </div>

          <dl className="definition-list">
            <div>
              <dt>Name</dt>
              <dd>{model.model_name}</dd>
            </div>
            <div>
              <dt>Architecture</dt>
              <dd>{model.architecture}</dd>
            </div>
            <div>
              <dt>Dataset</dt>
              <dd>{model.training_dataset}</dd>
            </div>
            <div>
              <dt>Training date</dt>
              <dd>{formatDateTime(model.training_date)}</dd>
            </div>
            <div>
              <dt>Active</dt>
              <dd>{model.is_active ? "Yes" : "No"}</dd>
            </div>
          </dl>
        </section>

        <section className="card">
          <div className="section-heading">
            <div>
              <span>Evaluation</span>
              <h2>Detection metrics</h2>
            </div>
          </div>

          {!hasMetrics ? (
            <div className="metrics-empty">
              <strong>Evaluation metrics are not added yet.</strong>
              <p>
                After training and test evaluation, update
                models/metadata/model_info.json in the backend with the real
                precision, recall, mAP@0.5 and mAP@0.5:0.95 values.
              </p>
            </div>
          ) : (
            <div className="metric-list">
              <MetricBar label="Precision" value={model.precision} />
              <MetricBar label="Recall" value={model.recall} />
              <MetricBar label="mAP@0.5" value={model.map50} />
              <MetricBar label="mAP@0.5:0.95" value={model.map50_95} />
            </div>
          )}
        </section>
      </div>

      <section className="card">
        <div className="section-heading">
          <div>
            <span>Detection labels</span>
            <h2>Road damage classes</h2>
          </div>
        </div>

        <div className="class-grid">
          {(model.classes || []).map((item) => (
            <article key={item.code} className={`class-card class-${item.code}`}>
              <span>{item.code}</span>
              <h3>{item.name}</h3>
            </article>
          ))}
        </div>
      </section>

      {hasMetrics && (
        <section className="card">
          <div className="section-heading">
            <div>
              <span>Summary</span>
              <h2>Recorded evaluation</h2>
            </div>
          </div>

          <div className="metric-summary-grid">
            <div>
              <span>Precision</span>
              <strong>{formatPercent(model.precision)}</strong>
            </div>
            <div>
              <span>Recall</span>
              <strong>{formatPercent(model.recall)}</strong>
            </div>
            <div>
              <span>mAP@0.5</span>
              <strong>{formatPercent(model.map50)}</strong>
            </div>
            <div>
              <span>mAP@0.5:0.95</span>
              <strong>{formatPercent(model.map50_95)}</strong>
            </div>
          </div>
        </section>
      )}
    </div>
  );
}
