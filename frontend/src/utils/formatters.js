// NEXUS Utility — Formatters
// Date, score, and display formatting helpers

export function formatDate(isoString) {
  if (!isoString) return '—';
  const d = new Date(isoString);
  return d.toLocaleDateString('en-US', { 
    month: 'short', day: 'numeric', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  });
}

export function formatScore(score) {
  if (score == null) return '—';
  return Math.round(score);
}

export function getRiskLevel(riskScore) {
  if (riskScore <= 20) return { label: 'Low', color: '#10b981' };
  if (riskScore <= 50) return { label: 'Medium', color: '#f59e0b' };
  if (riskScore <= 80) return { label: 'High', color: '#f97316' };
  return { label: 'Critical', color: '#ef4444' };
}

export function getScoreColor(score) {
  if (score >= 80) return '#10b981';
  if (score >= 60) return '#f59e0b';
  if (score >= 40) return '#f97316';
  return '#ef4444';
}

export function formatFileSize(bytes) {
  if (!bytes) return '0 B';
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

export function truncate(str, maxLen = 60) {
  if (!str || str.length <= maxLen) return str || '';
  return str.slice(0, maxLen) + '…';
}

export function groupBy(arr, key) {
  return arr.reduce((acc, item) => {
    const k = typeof key === 'function' ? key(item) : item[key];
    (acc[k] = acc[k] || []).push(item);
    return acc;
  }, {});
}

export function countBy(arr, key) {
  const groups = groupBy(arr, key);
  return Object.fromEntries(Object.entries(groups).map(([k, v]) => [k, v.length]));
}
