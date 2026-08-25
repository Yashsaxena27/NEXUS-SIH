import React from 'react';
import { CheckCircle, ShieldAlert, AlertCircle, HelpCircle } from 'lucide-react';

export default function FindingsList({ findings, passed, failed, unknown, onExplain }) {
  
  const getStatusIcon = (status) => {
    switch(status) {
      case 'PASS':
        return <CheckCircle color="var(--success-color)" />;
      case 'FAIL':
        return <ShieldAlert color="var(--error-color)" />;
      case 'UNKNOWN_ABSENT':
      case 'UNKNOWN_PARSE_ERROR':
      case 'UNKNOWN':
        return <HelpCircle color="var(--warning-color)" />;
      default:
        return <AlertCircle color="var(--text-secondary)" />;
    }
  };

  const getStatusText = (status) => {
    if (status === 'UNKNOWN_ABSENT') return 'Absent (Unknown)';
    if (status === 'UNKNOWN_PARSE_ERROR') return 'Parse Error (Unknown)';
    return status;
  };

  return (
    <div className="glass-panel" style={{ padding: '2rem' }}>
      <div className="flex justify-between items-center" style={{ marginBottom: '1.5rem' }}>
        <h2>Compliance Findings</h2>
        <div className="flex gap-2">
          <span className="badge badge-success">{passed} Passed</span>
          <span className="badge badge-error">{failed} Failed</span>
          {unknown > 0 && (
            <span className="badge badge-warning">{unknown} Unknown</span>
          )}
        </div>
      </div>
      
      <div className="grid gap-2" style={{ maxHeight: '600px', overflowY: 'auto', paddingRight: '0.5rem' }}>
        {findings.map((finding, idx) => (
          <div key={idx} className="glass-panel" style={{ padding: '1rem', border: '1px solid var(--surface-border)' }}>
            <div className="flex justify-between items-center gap-4">
              <div className="flex items-center gap-4" style={{ flex: 1 }}>
                <div style={{ flexShrink: 0 }}>
                  {getStatusIcon(finding.status)}
                </div>
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <h4 style={{ margin: 0 }}>{finding.control_id}</h4>
                    <span className="badge badge-neutral" style={{ fontSize: '0.65rem' }}>{finding.severity}</span>
                  </div>
                  <p style={{ margin: '0 0 0.25rem 0', fontWeight: 500 }}>{finding.control_title}</p>
                  <p style={{ margin: 0, fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                    <strong>Status:</strong> {getStatusText(finding.status)}
                  </p>
                </div>
              </div>
              <div style={{ flexShrink: 0 }}>
                {finding.status !== 'PASS' && (
                  <button 
                    className="btn btn-secondary" 
                    style={{ padding: '0.5rem 1rem' }}
                    onClick={() => onExplain(finding)}
                  >
                    View Details
                  </button>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
