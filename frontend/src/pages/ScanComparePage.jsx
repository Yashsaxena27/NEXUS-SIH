import React, { useEffect, useState } from 'react';
import { GitCompare, ArrowUp, ArrowDown, Minus } from 'lucide-react';
import { listScans, getScanDetail } from '../services/api';
import { VENDORS, SEVERITY_CONFIG } from '../utils/constants';
import { formatDate, formatScore, getScoreColor } from '../utils/formatters';

export default function ScanComparePage() {
  const [scans, setScans] = useState([]);
  const [scanA, setScanA] = useState('');
  const [scanB, setScanB] = useState('');
  const [detailA, setDetailA] = useState(null);
  const [detailB, setDetailB] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    listScans().then(setScans).catch(() => {});
  }, []);

  const compare = async () => {
    if (!scanA || !scanB) return;
    setLoading(true);
    setError(null);
    try {
      const [a, b] = await Promise.all([getScanDetail(scanA), getScanDetail(scanB)]);
      setDetailA(a);
      setDetailB(b);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const scoreDiff = detailA && detailB ? detailB.compliance_score - detailA.compliance_score : 0;

  // Compute finding diffs
  let fixed = [], newIssues = [], unchanged = [];
  if (detailA && detailB) {
    const bMap = new Map(detailB.findings.map(f => [f.control_id, f]));
    const aMap = new Map(detailA.findings.map(f => [f.control_id, f]));
    for (const [id, fA] of aMap) {
      const fB = bMap.get(id);
      if (!fB) continue;
      if (fA.status === 'FAIL' && fB.status === 'PASS') fixed.push({ control_id: id, title: fA.title, severity: fA.severity });
      else if (fA.status === 'PASS' && fB.status === 'FAIL') newIssues.push({ control_id: id, title: fB.title, severity: fB.severity });
      else unchanged.push({ control_id: id, title: fA.title, statusA: fA.status, statusB: fB.status });
    }
  }

  return (
    <div className="animate-fade-in">
      <div className="page-header"><h2>Scan Comparison</h2><p>Compare two scans to track security posture changes</p></div>

      <div className="glass-panel" style={{ padding: '1.25rem', marginBottom: '1.5rem' }}>
        <div className="grid grid-3 items-center">
          <div>
            <label className="input-label">Scan A (Before)</label>
            <select className="input" value={scanA} onChange={e => setScanA(e.target.value)}>
              <option value="">Select scan...</option>
              {scans.map(s => <option key={s.scan_id} value={s.scan_id}>{formatDate(s.created_at)} — {VENDORS[s.vendor]?.label || s.vendor} ({s.hostname || 'Unknown'})</option>)}
            </select>
          </div>
          <div className="text-center"><GitCompare size={24} style={{ color: 'var(--text-muted)' }} /></div>
          <div>
            <label className="input-label">Scan B (After)</label>
            <select className="input" value={scanB} onChange={e => setScanB(e.target.value)}>
              <option value="">Select scan...</option>
              {scans.map(s => <option key={s.scan_id} value={s.scan_id}>{formatDate(s.created_at)} — {VENDORS[s.vendor]?.label || s.vendor} ({s.hostname || 'Unknown'})</option>)}
            </select>
          </div>
        </div>
        <div className="text-center" style={{ marginTop: '1rem' }}>
          <button className="btn btn-primary" onClick={compare} disabled={!scanA || !scanB || loading}>
            {loading ? 'Comparing...' : 'Compare Scans'}
          </button>
        </div>
      </div>

      {error && <div className="error-banner">{error}</div>}

      {detailA && detailB && (
        <div className="animate-fade-in">
          <div className="grid grid-3" style={{ marginBottom: '1.5rem' }}>
            <div className="glass-panel stat-card text-center">
              <div className="stat-card-label">Score Change</div>
              <div className="stat-card-value" style={{ color: scoreDiff > 0 ? 'var(--success-color)' : scoreDiff < 0 ? 'var(--error-color)' : 'var(--text-secondary)' }}>
                {scoreDiff > 0 ? <ArrowUp size={20} style={{ display: 'inline' }} /> : scoreDiff < 0 ? <ArrowDown size={20} style={{ display: 'inline' }} /> : <Minus size={20} style={{ display: 'inline' }} />}
                {Math.abs(scoreDiff).toFixed(0)}
              </div>
              <div className="stat-card-sub">
                <span style={{ color: getScoreColor(detailA.compliance_score) }}>{formatScore(detailA.compliance_score)}</span>
                {' → '}
                <span style={{ color: getScoreColor(detailB.compliance_score) }}>{formatScore(detailB.compliance_score)}</span>
              </div>
              {scoreDiff > 0 && <span className="badge badge-success" style={{ marginTop: 8 }}>Improved</span>}
              {scoreDiff < 0 && <span className="badge badge-error" style={{ marginTop: 8 }}>Regressed</span>}
            </div>
            <div className="glass-panel stat-card text-center">
              <div className="stat-card-label">Fixed Issues</div>
              <div className="stat-card-value" style={{ color: 'var(--success-color)' }}>{fixed.length}</div>
              <div className="stat-card-sub">Controls moved FAIL → PASS</div>
            </div>
            <div className="glass-panel stat-card text-center">
              <div className="stat-card-label">New Issues</div>
              <div className="stat-card-value" style={{ color: 'var(--error-color)' }}>{newIssues.length}</div>
              <div className="stat-card-sub">Controls moved PASS → FAIL</div>
            </div>
          </div>

          {fixed.length > 0 && (
            <div className="glass-panel" style={{ padding: '1.25rem', marginBottom: '1rem' }}>
              <div className="stat-card-label" style={{ color: 'var(--success-color)', marginBottom: '0.5rem' }}>✓ Fixed</div>
              {fixed.map(f => (
                <div key={f.control_id} className="flex items-center gap-2" style={{ padding: '0.375rem 0', borderBottom: '1px solid var(--surface-border)' }}>
                  <span style={{ fontSize: '0.75rem', fontFamily: 'monospace', color: 'var(--text-muted)', width: 110 }}>{f.control_id}</span>
                  <span style={{ fontSize: '0.85rem', flex: 1 }}>{f.title}</span>
                  <span className="badge" style={{ background: SEVERITY_CONFIG[f.severity]?.bg, color: SEVERITY_CONFIG[f.severity]?.color, border: `1px solid ${SEVERITY_CONFIG[f.severity]?.border}` }}>{f.severity}</span>
                </div>
              ))}
            </div>
          )}

          {newIssues.length > 0 && (
            <div className="glass-panel" style={{ padding: '1.25rem' }}>
              <div className="stat-card-label" style={{ color: 'var(--error-color)', marginBottom: '0.5rem' }}>✗ New Issues</div>
              {newIssues.map(f => (
                <div key={f.control_id} className="flex items-center gap-2" style={{ padding: '0.375rem 0', borderBottom: '1px solid var(--surface-border)' }}>
                  <span style={{ fontSize: '0.75rem', fontFamily: 'monospace', color: 'var(--text-muted)', width: 110 }}>{f.control_id}</span>
                  <span style={{ fontSize: '0.85rem', flex: 1 }}>{f.title}</span>
                  <span className="badge" style={{ background: SEVERITY_CONFIG[f.severity]?.bg, color: SEVERITY_CONFIG[f.severity]?.color, border: `1px solid ${SEVERITY_CONFIG[f.severity]?.border}` }}>{f.severity}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {!detailA && !detailB && !loading && (
        <div className="empty-state">
          <div className="empty-state-icon"><GitCompare size={48} /></div>
          <div className="empty-state-title">Select Two Scans to Compare</div>
          <div className="empty-state-description">Choose a "before" and "after" scan to see how your security posture has changed.</div>
        </div>
      )}
    </div>
  );
}
