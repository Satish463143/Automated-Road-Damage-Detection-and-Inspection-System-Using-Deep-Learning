export function formatDateTime(value) {
  if (!value) return "N/A";

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "N/A";

  return new Intl.DateTimeFormat(undefined, {
    year: "numeric",
    month: "short",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
}

export function formatPercent(value, digits = 1) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return "N/A";
  }

  return `${(Number(value) * 100).toFixed(digits)}%`;
}

export function formatMilliseconds(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return "N/A";
  }

  const numeric = Number(value);

  if (numeric >= 1000) {
    return `${(numeric / 1000).toFixed(2)} s`;
  }

  return `${numeric.toFixed(0)} ms`;
}

export function formatNumber(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return "0";
  }

  return new Intl.NumberFormat().format(Number(value));
}

export function clamp(value, min = 0, max = 1) {
  return Math.min(Math.max(Number(value) || 0, min), max);
}
