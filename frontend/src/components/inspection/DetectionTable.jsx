import DamageBadge from "../ui/DamageBadge";
import { formatPercent } from "../../utils/format";

export default function DetectionTable({ detections = [] }) {
  if (!detections.length) {
    return (
      <div className="no-detections">
        No damage was detected above the configured confidence threshold.
      </div>
    );
  }

  return (
    <div className="table-wrap">
      <table className="data-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Damage</th>
            <th>Confidence</th>
            <th>Bounding box</th>
            <th>Area</th>
          </tr>
        </thead>

        <tbody>
          {detections.map((item, index) => (
            <tr key={item.id || `${item.damage_code}-${index}`}>
              <td>{index + 1}</td>
              <td>
                <DamageBadge
                  code={item.damage_code}
                  name={item.damage_name}
                />
              </td>
              <td>{formatPercent(item.confidence)}</td>
              <td className="mono-cell">
                {Math.round(item.x1)}, {Math.round(item.y1)} →{" "}
                {Math.round(item.x2)}, {Math.round(item.y2)}
              </td>
              <td>{Math.round(item.bounding_box_area).toLocaleString()} px²</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
