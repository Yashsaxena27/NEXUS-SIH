import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ClipboardCheck, ScanLine } from 'lucide-react';
import { useScan } from '../context/ScanContext';
import { STATUS_CONFIG } from '../utils/constants';

// Controls grouped by framework (derived from finding data)
export default function CompliancePage() {
  const navigate = useNavigate();
  const { currentScan } = useScan();
  const findings = currentScan?.findings || [];

  if (!currentScan) {
    return (
      <div className="empty-state animate-fade-in">
        <div className="empty-state-icon"><ClipboardCheck size={48} /></div>
        <div className="empty-state-title">No Compliance Data</div>
        <div className="empty-state-description">Run a scan to see compliance coverage across security frameworks.</div>
        <button className="btn btn-primary" onClick={() => navigate('/scan/new')}><ScanLine size={16} /> Start Scan</button>
      </div>
    );
  }

  // Group by framework
  const frameworkMap = {};
  findings.forEach(f => {
    const fws = f.frameworks || [];
    if (fws.length === 0) fws.push('General');
    fws.forEach(fw => {
      if (!frameworkMap[fw]) frameworkMap[fw] = [];
      frameworkMap[fw].push(f);
    });
  });

  // Also group by category
  const categoryMap = {};
  findings.forEach(f => {
    const cat = f.category || 'General';
    if (!categoryMap[cat]) categoryMap[cat] = [];
    categoryMap[cat].push(f);
  });

  return (
    <div className="animate-fade-in">
      <div className="page-header"><h2>Compliance Coverage</h2><p>Framework alignment for {currentScan.vendor} — {currentScan.hostname || 'Unknown Host'}</p></div>

      {/* Framework Cards */}
      <div className="grid grid-auto" style={{ marginBottom: '1.5rem' }}>
        {Object.entries(frameworkMap).map(([fw, controls]) => {
          const pass = controls.filter(c => c.status === 'PASS').length;
          const fail = controls.filter(c => c.status === 'FAIL').length;
          const unknown = controls.length - pass - fail;
          const pct = controls.length > 0 ? Math.round((pass / controls.length) * 100) : 0;
          return (
            <div key={fw} className="glass-panel" style={{ padding: '1.25rem' }}>
              <div className="flex justify-between items-center" style={{ marginBottom: '0.75rem' }}>
                <h3 style={{ fontSize: '1rem' }}>{fw}</h3>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{controls.length} controls</span>
              </div>
              <div style={{ marginBottom: '0.5rem' }}>
                <div className="flex justify-between" style={{ fontSize: '0.75rem', marginBottom: 4 }}>
                  <span style={{ color: 'var(--text-secondary)' }}>Compliance</span>
                  <span style={{ fontWeight: 600 }}>{pct}%</span>
                </div>
                <div style={{ height: 8, background: 'var(--surface-border)', borderRadius: 4, overflow: 'hidden' }}>
                  <div style={{ width: `${pct}%`, height: '100%', background: pct >= 80 ? 'var(--success-color)' : pct >= 50 ? 'var(--warning-color)' : 'var(--error-color)', borderRadius: 4, transition: 'width 0.6s ease' }} />
                </div>
              </div>
              <div className="flex gap-2">
                <span className="badge badge-success">{pass} Pass</span>
                <span className="badge badge-error">{fail} Fail</span>
                {unknown > 0 && <span className="badge badge-warning">{unknown} Unknown</span>}
              </div>
            </div>
          );
        })}
      </div>

      {/* Controls by Category */}
      <h3 style={{ marginBottom: '0.75rem', fontSize: '1rem' }}>Controls by Category</h3>
      {Object.entries(categoryMap).map(([cat, controls]) => (
        <div key={cat} className="glass-panel" style={{ padding: '1rem', marginBottom: '0.75rem' }}>
          <div className="flex justify-between items-center" style={{ marginBottom: '0.5rem' }}>
            <h4 style={{ fontSize: '0.9rem' }}>{cat}</h4>
            <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>{controls.length} controls</span>
          </div>
          {controls.map(f => {
            const s = STATUS_CONFIG[f.status] || STATUS_CONFIG.UNKNOWN;
            return (
              <div key={f.control_id} className="flex items-center gap-2" style={{ padding: '0.3rem 0', borderBottom: '1px solid rgba(255,255,255,0.03)' }}>
                <span style={{ width: 6, height: 6, borderRadius: '50%', background: s.color, flexShrink: 0 }} />
                <span style={{ fontSize: '0.7rem', fontFamily: 'monospace', color: 'var(--text-muted)', width: 100 }}>{f.control_id}</span>
                <span style={{ fontSize: '0.8rem', flex: 1 }}>{f.title || f.control_title}</span>
                <span className="badge" style={{ background: s.bg, color: s.color, border: `1px solid ${s.border}`, fontSize: '0.6rem' }}>{s.label}</span>
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
}
