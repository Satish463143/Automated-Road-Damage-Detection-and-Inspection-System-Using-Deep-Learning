import { DAMAGE_CLASS_LIST } from "../../data/damageClasses";
import { formatNumber } from "../../utils/format";

export default function DamageDistribution({ items = [] }) {
  const counts = Object.fromEntries(
    items.map((item) => [item.damage_code, Number(item.count) || 0])
  );

  const max = Math.max(
    1,
    ...DAMAGE_CLASS_LIST.map((item) => counts[item.code] || 0)
  );

  return (
    <div className="distribution-list">
      {DAMAGE_CLASS_LIST.map((damage) => {
        const count = counts[damage.code] || 0;
        const width = (count / max) * 100;

        return (
          <div className="distribution-row" key={damage.code}>
            <div className="distribution-label">
              <span className={`distribution-code code-${damage.code}`}>
                {damage.code}
              </span>
              <span>{damage.name}</span>
            </div>

            <div className="distribution-bar">
              <div
                className={`distribution-fill fill-${damage.code}`}
                style={{ width: `${width}%` }}
              />
            </div>

            <strong>{formatNumber(count)}</strong>
          </div>
        );
      })}
    </div>
  );
}
