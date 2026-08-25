import React from 'react';
import { X, Search } from 'lucide-react';
import AIExplanation from './AIExplanation';

export default function FindingDetail({ finding, onClose, onExplain, explaining, explanation }) {
  if (!finding) return null;

  const getStatusClass = (status) => {
    if (status === 'PASS') return 'badge-success';
    if (status === 'FAIL') return 'badge-error';
    return 'badge-warning';
  };

  const getStatusText = (status) => {
    if (status === 'UNKNOWN_ABSENT') return 'Absent (Unknown)';
    if (status === 'UNKNOWN_PARSE_ERROR') return 'Parse Error (Unknown)';
    return status;
  };

  return (
    <div style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.7)', zIndex: 50, display: 'flex', alignItems: 'center', justifyItems: 'center', justifyContent: 'center', padding: '2rem' }}>
      <div className="glass-panel animate-fade-in" style={{ width: '100%', maxWidth: '900px', maxHeight: '90vh', overflowY: 'auto', padding: '2rem', position: 'relative' }}>
        
        <button 
          onClick={onClose}
          style={{ position: 'absolute', top: '1.5rem', right: '1.5rem', background: 'transparent', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer' }}
        >
          <X size={24} />
        </button>

        <div style={{ marginBottom: '2rem', paddingRight: '2rem' }}>
          <div className="flex items-center gap-3 mb-2">
            <h2 style={{ margin: 0 }}>{finding.control_id}</h2>
            <span className={`badge ${getStatusClass(finding.status)}`}>{getStatusText(finding.status)}</span>
            <span className="badge badge-neutral">{finding.severity}</span>
          </div>
          <p style={{ fontSize: '1.125rem', color: 'var(--text-primary)', margin: 0 }}>{finding.control_title}</p>
        </div>

        <div className="grid grid-cols-2 gap-4" style={{ marginBottom: '2rem' }}>
          <div style={{ background: 'rgba(30, 41, 59, 0.5)', padding: '1rem', borderRadius: '0.5rem' }}>
            <h4 style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginBottom: '0.5rem', textTransform: 'uppercase' }}>What NEXUS Required</h4>
            <p style={{ margin: 0, fontFamily: 'monospace' }}>{JSON.stringify(finding.expected) || 'N/A'}</p>
          </div>
          <div style={{ background: 'rgba(30, 41, 59, 0.5)', padding: '1rem', borderRadius: '0.5rem' }}>
            <h4 style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginBottom: '0.5rem', textTransform: 'uppercase' }}>What NEXUS Found</h4>
            <p style={{ margin: 0, fontFamily: 'monospace' }}>{JSON.stringify(finding.actual) || 'Not present in configuration'}</p>
          </div>
        </div>

        <div style={{ marginBottom: '2rem' }}>
          <h4 style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginBottom: '0.5rem', textTransform: 'uppercase' }}>Evidence Context</h4>
          <div style={{ background: 'rgba(0,0,0,0.3)', padding: '1rem', borderRadius: '0.5rem', fontFamily: 'monospace', color: 'var(--text-primary)', whiteSpace: 'pre-wrap', overflowX: 'auto', fontSize: '0.875rem' }}>
            {finding.explanation_context || finding.evidence_raw || 'No evidence context available.'}
          </div>
        </div>

        {finding.remediation_hint && (
          <div style={{ marginBottom: '2rem' }}>
            <h4 style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginBottom: '0.5rem', textTransform: 'uppercase' }}>Deterministic Remediation Hint</h4>
            <p style={{ margin: 0 }}>{finding.remediation_hint}</p>
          </div>
        )}

        {finding.frameworks && finding.frameworks.length > 0 && (
          <div style={{ marginBottom: '2rem' }}>
            <h4 style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginBottom: '0.5rem', textTransform: 'uppercase' }}>Frameworks</h4>
            <div className="flex gap-2 flex-wrap">
              {finding.frameworks.map(fw => (
                <span key={fw} className="badge badge-neutral">{fw}</span>
              ))}
            </div>
          </div>
        )}

        {!explaining && !explanation && finding.status !== 'PASS' && (
          <div style={{ textAlign: 'center', marginTop: '2rem', borderTop: '1px solid var(--surface-border)', paddingTop: '2rem' }}>
            <button className="btn btn-primary" onClick={() => onExplain(finding)}>
              <Search size={18} /> Request AI Explanation
            </button>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginTop: '0.5rem' }}>
              Have Gemini analyze the configuration context and suggest a fix.
            </p>
          </div>
        )}

        {(explaining || explanation) && (
          <AIExplanation explaining={explaining} explanation={explanation} />
        )}

      </div>
    </div>
  );
}
