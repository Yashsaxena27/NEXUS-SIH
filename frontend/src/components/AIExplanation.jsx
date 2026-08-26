import React from 'react';
import { RefreshCw, Bot, ShieldCheck } from 'lucide-react';

export default function AIExplanation({ explaining, explanation }) {
  if (explaining) {
    return (
      <div style={{ textAlign: 'center', padding: '3rem', borderTop: '1px solid var(--surface-border)', marginTop: '2rem' }}>
        <RefreshCw className="spin" size={32} color="var(--accent-color)" style={{ margin: '0 auto 1rem', animation: 'spin 1s linear infinite' }} />
        <p>Gemini AI is analyzing the compliance violation...</p>
        <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
          Providing evidence-based interpretation and remediation steps.
        </p>
      </div>
    );
  }

  if (!explanation) return null;

  return (
    <div style={{ marginTop: '2rem', borderTop: '1px solid var(--surface-border)', paddingTop: '2rem' }}>
      <div className="flex items-center gap-2 mb-4">
        <Bot color="var(--accent-color)" />
        <h3 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          AI-Assisted Explanation
          <span className="badge badge-neutral" style={{ fontSize: '0.65rem' }}>Gemini</span>
        </h3>
      </div>
      
      <div style={{ marginBottom: '1rem', padding: '1rem', background: 'rgba(59, 130, 246, 0.05)', borderRadius: '0.5rem', borderLeft: '3px solid var(--accent-color)' }}>
        <p style={{ margin: 0, fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
          <em>NEXUS deterministic evaluation produced this security finding. AI is providing interpretation and suggesting remediation based on the configuration context.</em>
        </p>
      </div>

      <div style={{ marginBottom: '1.5rem' }}>
        <h4 style={{ color: 'var(--text-primary)', marginBottom: '0.5rem' }}>Interpretation</h4>
        <div style={{ color: 'var(--text-secondary)', lineHeight: 1.6, whiteSpace: 'pre-wrap' }}>
          {explanation.explanation}
        </div>
      </div>
      
      <div>
        <div className="flex items-center gap-2 mb-2">
          <ShieldCheck size={18} color="var(--success-color)" />
          <h4 style={{ color: 'var(--success-color)', margin: 0 }}>Recommended Remediation</h4>
        </div>
        <div style={{ background: 'rgba(0,0,0,0.3)', padding: '1rem', borderRadius: '0.5rem', fontFamily: 'monospace', color: 'var(--text-primary)', whiteSpace: 'pre-wrap', overflowX: 'auto' }}>
          {explanation.remediation}
        </div>
      </div>
    </div>
  );
}
