import StatCard from "../ui/StatCard";
import { DAMAGE_CLASS_LIST } from "../../data/damageClasses";
import {
  formatMilliseconds,
  formatPercent,
} from "../../utils/format";

export default function InspectionSummary({ inspection }) {
  const counts = Object.fromEntries(
    DAMAGE_CLASS_LIST.map((item) => [item.code, 0])
  );

  for (const detection of inspection?.detections || []) {
    if (detection.damage_code in counts) {
      counts[detection.damage_code] += 1;
    }
  }

  return (
    <>
      <div className="stats-grid stats-grid-six">
        <StatCard
          label="Total Damage"
          value={inspection?.total_detections ?? 0}
          helper="Detected objects"
        />

        {DAMAGE_CLASS_LIST.map((item) => (
          <StatCard
            key={item.code}
            label={item.shortName}
            value={counts[item.code]}
            code={item.code}
          />
        ))}

        <StatCard
          label="Avg. confidence"
          value={formatPercent(inspection?.average_confidence)}
          helper={formatMilliseconds(inspection?.processing_time_ms)}
        />
      </div>
    </>
  );
}
