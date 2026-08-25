import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ScanLine, ShieldAlert, TrendingUp, Server, ArrowRight } from 'lucide-react';
import { listScans, getScanDetail } from '../services/api';
import { SEVERITY_CONFIG, STATUS_CONFIG, VENDORS } from '../utils/constants';
import { formatDate, formatScore, getRiskLevel, getScoreColor, countBy } from '../utils/formatters';

export default function DashboardPage() {
  const navigate = useNavigate();
  const [scans, setScans] = useState(null);
  const [latestFindings, setLatestFindings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    try {
      setLoading(true);
      const data = await listScans();
      setScans(data);
      if (data.length > 0) {
        try {
          const detail = await getScanDetail(data[0].scan_id);
          setLatestFindings(detail.findings || []);
        } catch { /* latest findings optional */ }
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  if (loading) return <div className="loading-state"><div className="loading-spinner" /><span style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>Loading security overview...</span></div>;
  if (error) return <div className="error-banner"><ShieldAlert size={16} />{error}</div>;

  if (!scans || scans.length === 0) {
    return (
      <div className="empty-state animate-fade-in">
        <div className="empty-state-icon"><ScanLine size={48} /></div>
        <div className="empty-state-title">No Security Assessments Yet</div>
        <div className="empty-state-description">Upload a network device configuration to begin your first security compliance audit.</div>
        <button className="btn btn-primary" onClick={() => navigate('/scan/new')}>
          <ScanLine size={16} /> Start First Scan
        </button>
      </div>
    );
  }

  const avgScore = Math.round(scans.reduce((s, x) => s + x.compliance_score, 0) / scans.length);
  const avgRisk = Math.round(scans.reduce((s, x) => s + x.risk_score, 0) / scans.length);
  const riskLevel = getRiskLevel(avgRisk);
  const totalFailed = scans.reduce((s, x) => s + x.failed_controls, 0);
  const totalPassed = scans.reduce((s, x) => s + x.passed_controls, 0);
  const totalUnknown = scans.reduce((s, x) => s + x.unknown_controls, 0);
  const vendorCounts = countBy(scans, 'vendor');

  const sevCounts = { CRITICAL: 0, HIGH: 0, MEDIUM: 0, LOW: 0 };
  latestFindings.filter(f => f.status === 'FAIL').forEach(f => {
    if (sevCounts[f.severity] !== undefined) sevCounts[f.severity]++;
  });
  const maxSev = Math.max(...Object.values(sevCounts), 1);

  const topRisks = latestFindings.filter(f => f.status === 'FAIL').sort((a, b) => {
    const order = { CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3 };
    return (order[a.severity] ?? 4) - (order[b.severity] ?? 4);
  }).slice(0, 5);

  return (
    <div className="animate-fade-in">
      {/* Metric Cards */}
      <div className="grid grid-3" style={{ marginBottom: '1.5rem' }}>
        <div className="glass-panel stat-card animate-fade-in-up stagger-1">
          <div className="stat-card-label">Security Score</div>
          <div className="flex items-center gap-4">
            <div className="score-circle" style={{ '--score': avgScore, '--score-color': getScoreColor(avgScore), width: 100, height: 100 }}>
              <div className="score-circle-content">
                <div className="score-circle-value" style={{ fontSize: '1.5rem' }}>{avgScore}</div>
                <div className="score-circle-label">/ 100</div>
              </div>
            </div>
            <div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{scans.length} scan{scans.length !== 1 ? 's' : ''} analyzed</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: 2 }}>Avg compliance across all scans</div>
            </div>
          </div>
        </div>

        <div className="glass-panel stat-card animate-fade-in-up stagger-2">
          <div className="stat-card-label">Risk Level</div>
          <div className="stat-card-value" style={{ color: riskLevel.color }}>{riskLevel.label}</div>
          <div className="stat-card-sub">Risk score: {avgRisk}</div>
          <div style={{ marginTop: '0.75rem', display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            <span className="badge badge-success">{totalPassed} Passed</span>
            <span className="badge badge-error">{totalFailed} Failed</span>
            <span className="badge badge-warning">{totalUnknown} Unknown</span>
          </div>
        </div>

        <div className="glass-panel stat-card animate-fade-in-up stagger-3">
          <div className="stat-card-label">Compliance Coverage</div>
          <div style={{ marginTop: '0.5rem' }}>
            <div className="flex justify-between" style={{ fontSize: '0.8rem', marginBottom: 4 }}>
              <span style={{ color: 'var(--text-secondary)' }}>Pass Rate</span>
              <span style={{ fontWeight: 600 }}>{totalPassed + totalFailed > 0 ? Math.round(totalPassed / (totalPassed + totalFailed) * 100) : 0}%</span>
            </div>
            <div style={{ height: 8, background: 'var(--surface-border)', borderRadius: 4, overflow: 'hidden' }}>
              <div style={{ width: `${totalPassed + totalFailed > 0 ? totalPassed / (totalPassed + totalFailed) * 100 : 0}%`, height: '100%', background: 'var(--success-color)', borderRadius: 4, transition: 'width 0.8s ease' }} />
            </div>
          </div>
          <div style={{ marginTop: '0.75rem' }}>
            {Object.entries(vendorCounts).map(([v, c]) => (
              <div key={v} className="flex items-center gap-2" style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: 4 }}>
                <span style={{ width: 8, height: 8, borderRadius: '50%', background: VENDORS[v]?.color || '#6b7280', flexShrink: 0 }} />
                {VENDORS[v]?.label || v}: {c}
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="grid grid-2" style={{ marginBottom: '1.5rem' }}>
        {/* Risk Distribution */}
        <div className="glass-panel animate-fade-in-up stagger-4" style={{ padding: '1.25rem' }}>
          <div className="stat-card-label" style={{ marginBottom: '0.75rem' }}>Risk Distribution (Latest Scan)</div>
          {Object.entries(sevCounts).map(([sev, count]) => (
            <div key={sev} className="flex items-center gap-2" style={{ marginBottom: '0.5rem' }}>
              <span style={{ width: 70, fontSize: '0.75rem', color: 'var(--text-secondary)' }}>{SEVERITY_CONFIG[sev]?.label || sev}</span>
              <div style={{ flex: 1, height: 8, background: 'var(--surface-border)', borderRadius: 4, overflow: 'hidden' }}>
                <div style={{ width: `${maxSev > 0 ? (count / maxSev) * 100 : 0}%`, height: '100%', background: SEVERITY_CONFIG[sev]?.color, borderRadius: 4, transition: 'width 0.6s ease' }} />
              </div>
              <span style={{ width: 24, fontSize: '0.8rem', textAlign: 'right', fontWeight: 600 }}>{count}</span>
            </div>
          ))}
        </div>

        {/* Top Risks */}
        <div className="glass-panel animate-fade-in-up stagger-5" style={{ padding: '1.25rem' }}>
          <div className="flex justify-between items-center" style={{ marginBottom: '0.75rem' }}>
            <div className="stat-card-label" style={{ margin: 0 }}>Top Security Risks</div>
            {latestFindings.length > 0 && <button className="btn btn-ghost btn-sm" onClick={() => navigate('/findings')}>View All <ArrowRight size={14} /></button>}
          </div>
          {topRisks.length === 0 && <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', padding: '1rem 0' }}>No failed controls in latest scan</div>}
          {topRisks.map(f => (
            <div key={f.control_id} className="finding-row" style={{ marginBottom: '0.375rem', padding: '0.625rem 0.75rem' }} onClick={() => navigate(`/findings/${f.control_id}`)}>
              <div className="finding-row-status" style={{ background: SEVERITY_CONFIG[f.severity]?.color || '#6b7280' }} />
              <div className="finding-row-content">
                <div className="finding-row-id">{f.control_id}</div>
                <div className="finding-row-title" style={{ fontSize: '0.8rem' }}>{f.title}</div>
              </div>
              <span className="badge" style={{ background: SEVERITY_CONFIG[f.severity]?.bg, color: SEVERITY_CONFIG[f.severity]?.color, border: `1px solid ${SEVERITY_CONFIG[f.severity]?.border}` }}>{f.severity}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Scans */}
      <div className="glass-panel animate-fade-in-up" style={{ padding: '1.25rem' }}>
        <div className="flex justify-between items-center" style={{ marginBottom: '0.75rem' }}>
          <div className="stat-card-label" style={{ margin: 0 }}>Recent Scans</div>
          <button className="btn btn-ghost btn-sm" onClick={() => navigate('/history')}>View All <ArrowRight size={14} /></button>
        </div>
        <table className="data-table">
          <thead>
            <tr><th>Date</th><th>Vendor</th><th>Hostname</th><th>Score</th><th>Risk</th><th>Findings</th></tr>
          </thead>
          <tbody>
            {scans.slice(0, 5).map(s => {
              const rl = getRiskLevel(s.risk_score);
              return (
                <tr key={s.scan_id} onClick={() => navigate(`/scan/${s.scan_id}`)}>
                  <td style={{ color: 'var(--text-primary)' }}>{formatDate(s.created_at)}</td>
                  <td><span className="flex items-center gap-2"><span style={{ width: 8, height: 8, borderRadius: '50%', background: VENDORS[s.vendor]?.color || '#6b7280' }} />{VENDORS[s.vendor]?.label || s.vendor}</span></td>
                  <td>{s.hostname || 'Unknown'}</td>
                  <td style={{ color: getScoreColor(s.compliance_score), fontWeight: 600 }}>{formatScore(s.compliance_score)}</td>
                  <td><span style={{ color: rl.color, fontSize: '0.8rem', fontWeight: 500 }}>{rl.label}</span></td>
                  <td><span style={{ fontSize: '0.75rem' }}>{s.passed_controls}P / {s.failed_controls}F / {s.unknown_controls}U</span></td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
