import React from 'react';
import { Cpu, Settings, Activity } from 'lucide-react';

export default function ScoreSummary({ result, onReset }) {
  return (
    <div className="grid gap-4">
      <div className="glass-panel" style={{ padding: '1.5rem' }}>
        <h3 style={{ marginBottom: '1.5rem', textAlign: 'center' }}>Security Score</h3>
        <div className="flex justify-center" style={{ marginBottom: '1rem' }}>
          <div className="score-circle" style={{ '--score': result.compliance_score }}>
            <div className="score-content">
              <span style={{ fontSize: '2rem', fontWeight: 700 }}>{Math.round(result.compliance_score)}</span>
              <span style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', display: 'block' }}>/ 100</span>
            </div>
          </div>
        </div>
        <div style={{ textAlign: 'center', marginTop: '1rem' }}>
          <p style={{ margin: 0, color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Risk Score: {Math.round(result.risk_score)} / 100</p>
        </div>
      </div>

      <div className="glass-panel" style={{ padding: '1.5rem' }}>
        <h3 style={{ marginBottom: '1rem' }}>Device Profile</h3>
        <div className="flex items-center gap-2" style={{ marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>
          <Cpu size={16} /> <span>Vendor: </span> <strong style={{ color: 'var(--text-primary)', textTransform: 'capitalize' }}>{result.vendor}</strong>
        </div>
        <div className="flex items-center gap-2" style={{ marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>
          <Settings size={16} /> <span>OS: </span> <strong style={{ color: 'var(--text-primary)' }}>{result.platform || 'Unknown'}</strong>
        </div>
        <div className="flex items-center gap-2" style={{ color: 'var(--text-secondary)' }}>
          <Activity size={16} /> <span>Host: </span> <strong style={{ color: 'var(--text-primary)' }}>{result.hostname || 'Unknown'}</strong>
        </div>
      </div>
      
      <button 
        className="btn btn-secondary"
        onClick={onReset}
        style={{ width: '100%' }}
      >
        Scan Another Configuration
      </button>
    </div>
  );
}
