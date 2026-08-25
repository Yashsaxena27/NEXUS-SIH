import React, { useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { FileText, Printer, ScanLine } from 'lucide-react';
import { useScan } from '../context/ScanContext';
import { SEVERITY_CONFIG, STATUS_CONFIG, VENDORS } from '../utils/constants';
import { formatDate, formatScore, getScoreColor, getRiskLevel } from '../utils/formatters';

export default function ReportsPage() {
  const navigate = useNavigate();
  const { currentScan } = useScan();
  const reportRef = useRef();

  if (!currentScan) {
    return (
      <div className="empty-state animate-fade-in">
        <div className="empty-state-icon"><FileText size={48} /></div>
        <div className="empty-state-title">No Report Data</div>
        <div className="empty-state-description">Run a scan to generate a security assessment report.</div>
        <button className="btn btn-primary" onClick={() => navigate('/scan/new')}><ScanLine size={16} /> Start Scan</button>
      </div>
    );
  }

  const findings = currentScan.findings || [];
  const fails = findings.filter(f => f.status === 'FAIL');
  const rl = getRiskLevel(currentScan.risk_score);
  const vendor = VENDORS[currentScan.vendor] || VENDORS.unknown;

  const handlePrint = () => window.print();

  return (
    <div className="animate-fade-in">
      <div className="flex justify-between items-center" style={{ marginBottom: '1.5rem' }}>
        <div className="page-header" style={{ margin: 0 }}><h2>Security Assessment Report</h2><p>{vendor.label} • {currentScan.hostname || 'Unknown Host'}</p></div>
        <button className="btn btn-secondary" onClick={handlePrint}><Printer size={16} /> Print Report</button>
      </div>

      <div ref={reportRef}>
        {/* Executive Summary */}
        <div className="glass-panel" style={{ padding: '1.5rem', marginBottom: '1rem' }}>
          <h3 style={{ fontSize: '1.1rem', marginBottom: '1rem' }}>Executive Summary</h3>
          <div className="grid grid-4 gap-4">
            <div><div className="stat-card-label">Security Score</div><div style={{ fontSize: '1.5rem', fontWeight: 700, color: getScoreColor(currentScan.compliance_score) }}>{formatScore(currentScan.compliance_score)} / 100</div></div>
            <div><div className="stat-card-label">Risk Level</div><div style={{ fontSize: '1.5rem', fontWeight: 700, color: rl.color }}>{rl.label}</div></div>
            <div><div className="stat-card-label">Controls Evaluated</div><div style={{ fontSize: '1.5rem', fontWeight: 700 }}>{currentScan.total_controls}</div></div>
            <div><div className="stat-card-label">Failed Controls</div><div style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--error-color)' }}>{currentScan.failed_controls}</div></div>
          </div>
          <div style={{ marginTop: '1rem', fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: 1.7 }}>
            NEXUS performed a deterministic compliance audit of the {vendor.label} device configuration
            {currentScan.hostname ? ` (${currentScan.hostname})` : ''}. The analysis evaluated {currentScan.total_controls} security controls
            against CIS and NIST benchmarks. {currentScan.passed_controls} controls passed, {currentScan.failed_controls} controls failed,
            and {currentScan.unknown_controls} controls could not be determined. {fails.length > 0 ? `The following section details all ${fails.length} failed controls with remediation guidance.` : 'All evaluated controls are compliant.'}
          </div>
        </div>

        {/* Findings Detail */}
        {fails.length > 0 && (
          <div className="glass-panel" style={{ padding: '1.5rem', marginBottom: '1rem' }}>
            <h3 style={{ fontSize: '1.1rem', marginBottom: '1rem' }}>Failed Controls</h3>
            {fails.sort((a, b) => {
              const o = { CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3 };
              return (o[a.severity] ?? 4) - (o[b.severity] ?? 4);
            }).map((f, i) => (
              <div key={f.control_id} style={{ padding: '0.75rem 0', borderBottom: i < fails.length - 1 ? '1px solid var(--surface-border)' : 'none' }}>
                <div className="flex items-center gap-2" style={{ marginBottom: '0.25rem' }}>
                  <span style={{ fontSize: '0.75rem', fontFamily: 'monospace', color: 'var(--text-muted)' }}>{f.control_id}</span>
                  <span className="badge" style={{ background: SEVERITY_CONFIG[f.severity]?.bg, color: SEVERITY_CONFIG[f.severity]?.color, border: `1px solid ${SEVERITY_CONFIG[f.severity]?.border}` }}>{f.severity}</span>
                </div>
                <div style={{ fontWeight: 500, marginBottom: '0.25rem' }}>{f.title || f.control_title}</div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                  Expected: <code>{f.expected || 'N/A'}</code> • Found: <code>{f.actual || 'N/A'}</code>
                </div>
                {f.remediation_hint && <div style={{ fontSize: '0.8rem', color: 'var(--success-color)', marginTop: '0.25rem' }}>Remediation: {f.remediation_hint}</div>}
              </div>
            ))}
          </div>
        )}

        {/* Passed Controls */}
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <h3 style={{ fontSize: '1.1rem', marginBottom: '0.75rem' }}>Passed Controls ({currentScan.passed_controls})</h3>
          <div className="grid grid-2">
            {findings.filter(f => f.status === 'PASS').map(f => (
              <div key={f.control_id} className="flex items-center gap-2" style={{ padding: '0.25rem 0' }}>
                <span style={{ width: 6, height: 6, borderRadius: '50%', background: 'var(--success-color)', flexShrink: 0 }} />
                <span style={{ fontSize: '0.75rem', fontFamily: 'monospace', color: 'var(--text-muted)' }}>{f.control_id}</span>
                <span style={{ fontSize: '0.8rem' }}>{f.title || f.control_title}</span>
              </div>
            ))}
          </div>
        </div>

        <div style={{ textAlign: 'center', margin: '2rem 0', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
          Report generated by NEXUS — Network Security Compliance Auditor • {new Date().toLocaleDateString()}
        </div>
      </div>
    </div>
  );
}
