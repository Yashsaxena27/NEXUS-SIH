import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { History, ScanLine, ShieldCheck, AlertTriangle, Loader } from 'lucide-react';
import { listScans, API_BASE_URL } from '../services/api';
import { VENDORS } from '../utils/constants';
import { formatDate, formatScore, getScoreColor, getRiskLevel } from '../utils/formatters';

export default function ScanHistoryPage() {
  const navigate = useNavigate();
  const [scans, setScans] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const [auditStatus, setAuditStatus] = useState(null); // null, 'loading', 'verified', 'tampered'
  const [auditMessage, setAuditMessage] = useState("");

  useEffect(() => {
    listScans().then(setScans).catch(e => setError(e.message)).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading-state"><div className="loading-spinner" /></div>;
  if (error) return <div className="error-banner">{error}</div>;

  if (!scans?.length) {
    return (
      <div className="empty-state animate-fade-in">
        <div className="empty-state-icon"><History size={48} /></div>
        <div className="empty-state-title">No Scan History</div>
        <div className="empty-state-description">Your completed security scans will appear here.</div>
        <button className="btn btn-primary" onClick={() => navigate('/scan/new')}><ScanLine size={16} /> Start Scan</button>
      </div>
    );
  }

  const verifyAudit = async () => {
    setAuditStatus('loading');
    try {
      const res = await fetch(`${API_BASE_URL}/audit/verify`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
      });
      const data = await res.json();
      if (data.status === "VERIFIED") {
        setAuditStatus('verified');
      } else {
        setAuditStatus('tampered');
      }
      setAuditMessage(data.message);
    } catch (err) {
      setAuditStatus('error');
      setAuditMessage(err.message);
    }
  };

  return (
    <div className="animate-fade-in">
      <div className="page-header flex justify-between items-center" style={{ marginBottom: '1.5rem' }}>
        <div>
          <h2>Scan History</h2>
          <p>{scans.length} scan{scans.length !== 1 ? 's' : ''} completed</p>
        </div>
        <button 
          className="btn" 
          onClick={verifyAudit} 
          disabled={auditStatus === 'loading'}
          style={{ 
            background: 'rgba(16, 185, 129, 0.1)', 
            color: 'var(--success-color)', 
            border: '1px solid rgba(16, 185, 129, 0.2)' 
          }}
        >
          {auditStatus === 'loading' ? <Loader size={16} className="animate-spin" /> : <ShieldCheck size={16} />}
          Verify Audit Trail
        </button>
      </div>

      {auditStatus && auditStatus !== 'loading' && (
        <div className={`glass-panel`} style={{ padding: '1rem', marginBottom: '1rem', borderColor: auditStatus === 'verified' ? 'var(--success-color)' : 'var(--error-color)' }}>
          <div className="flex items-center gap-2" style={{ color: auditStatus === 'verified' ? 'var(--success-color)' : 'var(--error-color)', marginBottom: '0.25rem' }}>
            {auditStatus === 'verified' ? <ShieldCheck size={18} /> : <AlertTriangle size={18} />}
            <span style={{ fontWeight: 600 }}>{auditStatus === 'verified' ? 'Audit Chain Verified' : 'Integrity Violation Detected'}</span>
          </div>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>{auditMessage}</p>
        </div>
      )}

      <div className="glass-panel" style={{ padding: '0.5rem', overflow: 'auto' }}>
        <table className="data-table">
          <thead><tr><th>Date</th><th>Name</th><th>Vendor</th><th>Host</th><th>Score</th><th>Risk</th><th>Controls</th></tr></thead>
          <tbody>
            {scans.map(s => {
              const rl = getRiskLevel(s.risk_score);
              return (
                <tr key={s.scan_id} onClick={() => navigate(`/scan/${s.scan_id}`)}>
                  <td style={{ color: 'var(--text-primary)', whiteSpace: 'nowrap' }}>{formatDate(s.created_at)}</td>
                  <td>{s.scan_name || '—'}</td>
                  <td><span className="flex items-center gap-2"><span style={{ width: 8, height: 8, borderRadius: '50%', background: VENDORS[s.vendor]?.color || '#6b7280', flexShrink: 0 }} />{VENDORS[s.vendor]?.label || s.vendor}</span></td>
                  <td>{s.hostname || 'Unknown'}</td>
                  <td style={{ color: getScoreColor(s.compliance_score), fontWeight: 600 }}>{formatScore(s.compliance_score)}</td>
                  <td><span style={{ color: rl.color, fontWeight: 500 }}>{rl.label}</span></td>
                  <td style={{ fontSize: '0.75rem' }}>{s.passed_controls}P / {s.failed_controls}F / {s.unknown_controls}U</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
