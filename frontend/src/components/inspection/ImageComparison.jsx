import { toAbsoluteMediaUrl } from "../../services/api";

export default function ImageComparison({
  originalUrl,
  resultUrl,
}) {
  const original = toAbsoluteMediaUrl(originalUrl);
  const result = toAbsoluteMediaUrl(resultUrl);

  return (
    <div className="image-comparison-grid">
      <article className="image-panel">
        <div className="panel-heading">
          <div>
            <span>Input</span>
            <h3>Original image</h3>
          </div>
        </div>

        {original ? (
          <img src={original} alt="Original road inspection" />
        ) : (
          <div className="image-placeholder">Original image unavailable</div>
        )}
      </article>

      <article className="image-panel">
        <div className="panel-heading">
          <div>
            <span>Model output</span>
            <h3>Detected damage</h3>
          </div>
        </div>

        {result ? (
          <img src={result} alt="Road damage detections" />
        ) : (
          <div className="image-placeholder">
            Annotated image unavailable
          </div>
        )}
      </article>
    </div>
  );
}
