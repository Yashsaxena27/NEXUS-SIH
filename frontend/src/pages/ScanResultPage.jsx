import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { CheckCircle, ArrowRight, ShieldAlert } from 'lucide-react';
import { useScan } from '../context/ScanContext';
import { getScanDetail } from '../services/api';
import { SEVERITY_CONFIG, STATUS_CONFIG, VENDORS } from '../utils/constants';
import { formatScore, getScoreColor, getRiskLevel } from '../utils/formatters';

export default function ScanResultPage() {
  const navigate = useNavigate();
  const { scanId } = useParams();
  const { currentScan, setScanResult } = useScan();
  const [scan, setScan] = useState(currentScan);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (currentScan) { setScan(currentScan); return; }
    if (scanId) {
      setLoading(true);
      getScanDetail(scanId).then(d => { setScan(d); setScanResult(d); }).catch(e => setError(e.message)).finally(() => setLoading(false));
    }
  }, [scanId, currentScan]);

  if (loading) return <div className="loading-state"><div className="loading-spinner" /></div>;
  if (error) return <div className="error-banner"><ShieldAlert size={16} />{error}</div>;
  if (!scan) return <div className="empty-state"><div className="empty-state-title">No scan data</div><div className="empty-state-description">Run a scan first to see results.</div><button className="btn btn-primary" onClick={() => navigate('/scan/new')}>New Scan</button></div>;

  const findings = scan.findings || [];
  const failFindings = findings.filter(f => (f.status === 'FAIL'));
  const riskLevel = getRiskLevel(scan.risk_score);
  const scoreColor = getScoreColor(scan.compliance_score);

  const sevCounts = { CRITICAL: 0, HIGH: 0, MEDIUM: 0, LOW: 0 };
  failFindings.forEach(f => { if (sevCounts[f.severity] !== undefined) sevCounts[f.severity]++; });
  const maxSev = Math.max(...Object.values(sevCounts), 1);

  const topRisks = failFindings.sort((a, b) => {
    const o = { CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3 };
    return (o[a.severity] ?? 4) - (o[b.severity] ?? 4);
  }).slice(0, 5);

  return (
    <div className="animate-fade-in">
      <div className="text-center" style={{ marginBottom: '2rem' }}>
        <CheckCircle size={40} style={{ color: 'var(--success-color)', marginBottom: '0.5rem' }} />
        <h2 style={{ marginBottom: '0.25rem' }}>Scan Complete</h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
          {VENDORS[scan.vendor]?.label || scan.vendor} • {scan.hostname || 'Unknown Host'} • {scan.platform || ''}
        </p>
      </div>

      <div className="grid grid-3" style={{ marginBottom: '1.5rem' }}>
        <div className="glass-panel stat-card text-center animate-fade-in-up stagger-1">
          <div className="stat-card-label">Security Score</div>
          <div className="score-circle" style={{ '--score': scan.compliance_score, '--score-color': scoreColor, margin: '0.75rem auto' }}>
            <div className="score-circle-content">
              <div className="score-circle-value" style={{ color: scoreColor }}>{formatScore(scan.compliance_score)}</div>
              <div className="score-circle-label">/ 100</div>
            </div>
          </div>
        </div>
        <div className="glass-panel stat-card animate-fade-in-up stagger-2">
          <div className="stat-card-label">Risk Assessment</div>
          <div className="stat-card-value" style={{ color: riskLevel.color, marginBottom: '0.5rem' }}>{riskLevel.label}</div>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Risk Score: {scan.risk_score}</div>
          <div style={{ marginTop: '0.75rem', display: 'flex', gap: '0.375rem', flexWrap: 'wrap' }}>
            <span className="badge badge-success">{scan.passed_controls} Pass</span>
            <span className="badge badge-error">{scan.failed_controls} Fail</span>
            <span className="badge badge-warning">{scan.unknown_controls} Unknown</span>
          </div>
        </div>
        <div className="glass-panel stat-card animate-fade-in-up stagger-3">
          <div className="stat-card-label">Severity Breakdown</div>
          {Object.entries(sevCounts).map(([sev, count]) => (
            <div key={sev} className="flex items-center gap-2" style={{ marginBottom: '0.375rem' }}>
              <span style={{ width: 60, fontSize: '0.7rem', color: 'var(--text-secondary)' }}>{SEVERITY_CONFIG[sev]?.label}</span>
              <div style={{ flex: 1, height: 6, background: 'var(--surface-border)', borderRadius: 3, overflow: 'hidden' }}>
                <div style={{ width: `${(count / maxSev) * 100}%`, height: '100%', background: SEVERITY_CONFIG[sev]?.color, borderRadius: 3 }} />
              </div>
              <span style={{ width: 20, fontSize: '0.75rem', textAlign: 'right', fontWeight: 600 }}>{count}</span>
            </div>
          ))}
        </div>
      </div>

      {topRisks.length > 0 && (
        <div className="glass-panel animate-fade-in-up" style={{ padding: '1.25rem', marginBottom: '1.5rem' }}>
          <div className="stat-card-label" style={{ marginBottom: '0.75rem' }}>Top Security Risks</div>
          {topRisks.map(f => (
            <div key={f.control_id} className="finding-row" style={{ marginBottom: '0.375rem' }} onClick={() => navigate(`/findings/${f.control_id}`)}>
              <div className="finding-row-status" style={{ background: SEVERITY_CONFIG[f.severity]?.color }} />
              <div className="finding-row-content">
                <div className="finding-row-id">{f.control_id}</div>
                <div className="finding-row-title">{f.title}</div>
              </div>
              <span className="badge" style={{ background: SEVERITY_CONFIG[f.severity]?.bg, color: SEVERITY_CONFIG[f.severity]?.color, border: `1px solid ${SEVERITY_CONFIG[f.severity]?.border}` }}>{f.severity}</span>
            </div>
          ))}
        </div>
      )}

      <div className="flex justify-center gap-3">
        <button className="btn btn-primary" onClick={() => navigate('/findings')}><ShieldAlert size={16} /> View All Findings</button>
        <button className="btn btn-secondary" onClick={() => navigate('/scan/new')}>New Scan</button>
      </div>
    </div>
  );
}
