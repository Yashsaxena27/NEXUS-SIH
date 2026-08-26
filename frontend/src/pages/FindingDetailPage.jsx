import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft, Shield, Bot, Loader, RefreshCw, AlertTriangle } from 'lucide-react';
import { useScan } from '../context/ScanContext';
import { explainFinding } from '../services/api';
import { SEVERITY_CONFIG, STATUS_CONFIG, STATUS_DESCRIPTIONS } from '../utils/constants';

export default function FindingDetailPage() {
  const navigate = useNavigate();
  const { controlId } = useParams();
  const { currentScan } = useScan();
  const [aiResult, setAiResult] = useState(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiError, setAiError] = useState(null);

  const findings = currentScan?.findings || [];
  const finding = findings.find(f => f.control_id === controlId);

  if (!finding) {
    return (
      <div className="empty-state animate-fade-in">
        <div className="empty-state-icon"><AlertTriangle size={48} /></div>
        <div className="empty-state-title">Finding Not Found</div>
        <div className="empty-state-description">Control "{controlId}" not found in current scan data. Run a scan first.</div>
        <button className="btn btn-secondary" onClick={() => navigate('/findings')}><ArrowLeft size={16} /> Back to Findings</button>
      </div>
    );
  }

  const statusCfg = STATUS_CONFIG[finding.status] || STATUS_CONFIG.UNKNOWN;
  const sevCfg = SEVERITY_CONFIG[finding.severity] || SEVERITY_CONFIG.LOW;
  const frameworks = finding.frameworks || [];
  const frameworkMappings = finding.framework_mappings || [];

  const requestAI = async () => {
    setAiLoading(true);
    setAiError(null);
    try {
      const data = await explainFinding(
        finding, currentScan.platform || currentScan.vendor,
        finding.explanation_context || finding.evidence_raw || ''
      );
      setAiResult(data);
    } catch (err) {
      setAiError(err.message);
    } finally {
      setAiLoading(false);
    }
  };

  return (
    <div className="animate-fade-in" style={{ maxWidth: 800, margin: '0 auto' }}>
      <button className="btn btn-ghost" onClick={() => navigate('/findings')} style={{ marginBottom: '1rem' }}>
        <ArrowLeft size={16} /> Back to Findings
      </button>

      {/* Header */}
      <div className="glass-panel" style={{ padding: '1.5rem', marginBottom: '1rem' }}>
        <div className="flex items-center gap-2" style={{ marginBottom: '0.5rem' }}>
          <span className="finding-row-id" style={{ fontSize: '0.8rem' }}>{finding.control_id}</span>
          <span className="badge" style={{ background: statusCfg.bg, color: statusCfg.color, border: `1px solid ${statusCfg.border}` }}>{statusCfg.label}</span>
          <span className="badge" style={{ background: sevCfg.bg, color: sevCfg.color, border: `1px solid ${sevCfg.border}` }}>{sevCfg.label}</span>
        </div>
        <h2 style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>{finding.title || finding.control_title}</h2>
        <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
          {STATUS_DESCRIPTIONS[finding.status] || ''}
        </p>
        {frameworks.length > 0 && frameworkMappings.length === 0 && (
          <div className="flex gap-1" style={{ marginTop: '0.75rem', flexWrap: 'wrap' }}>
            {frameworks.map(fw => <span key={fw} className="badge badge-info">{fw}</span>)}
          </div>
        )}
        
        {frameworkMappings.length > 0 && (
          <div className="flex flex-col gap-2" style={{ marginTop: '0.75rem' }}>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Framework Mappings</div>
            {frameworkMappings.map((mapping, idx) => (
              <div key={idx} className="flex items-center gap-2" style={{ fontSize: '0.8rem' }}>
                <span className="badge badge-info">{mapping.framework}</span>
                <span style={{ fontFamily: 'monospace' }}>{mapping.control_id}</span>
                <span className="badge" style={{ background: mapping.mapping_type === 'DIRECT' ? 'rgba(16, 185, 129, 0.1)' : 'rgba(245, 158, 11, 0.1)', color: mapping.mapping_type === 'DIRECT' ? 'var(--success-color)' : 'var(--warning-color)' }}>
                  {mapping.mapping_type}
                </span>
                <span style={{ color: 'var(--text-muted)' }}>({mapping.source})</span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Deterministic Section */}
      <div style={{ marginBottom: '0.75rem' }}>
        <div className="flex items-center gap-2" style={{ marginBottom: '0.5rem' }}>
          <Shield size={16} style={{ color: 'var(--accent-color)' }} />
          <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--accent-color)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>NEXUS Deterministic Finding</span>
        </div>
      </div>

      <div className="grid grid-2" style={{ marginBottom: '1rem' }}>
        <div className="glass-panel" style={{ padding: '1rem' }}>
          <div className="stat-card-label">Expected State</div>
          <code style={{ fontSize: '0.85rem', color: 'var(--success-color)', wordBreak: 'break-all' }}>{finding.expected ?? 'N/A'}</code>
        </div>
        <div className="glass-panel" style={{ padding: '1rem' }}>
          <div className="stat-card-label">Actual State Found</div>
          <code style={{ fontSize: '0.85rem', color: finding.status === 'PASS' ? 'var(--success-color)' : 'var(--error-color)', wordBreak: 'break-all' }}>{finding.actual ?? 'N/A'}</code>
        </div>
      </div>

      {/* Evidence */}
      <div className="glass-panel" style={{ padding: '1rem', marginBottom: '1rem' }}>
        <div className="stat-card-label">Evidence</div>
        <div className="grid grid-2 gap-3" style={{ marginTop: '0.5rem' }}>
          <div><span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Field</span><p style={{ fontSize: '0.85rem' }}>{finding.evidence_field || 'N/A'}</p></div>
          <div><span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Source</span><p style={{ fontSize: '0.85rem' }}>{finding.evidence_source || 'N/A'}</p></div>
          <div><span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Confidence</span><p style={{ fontSize: '0.85rem' }}>{Math.round((finding.confidence || 0) * 100)}%</p></div>
          {finding.evidence_raw && <div><span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Raw</span><p style={{ fontSize: '0.8rem', fontFamily: 'monospace', wordBreak: 'break-all' }}>{finding.evidence_raw}</p></div>}
        </div>
      </div>

      {/* Context */}
      {finding.explanation_context && (
        <div className="glass-panel" style={{ padding: '1rem', marginBottom: '1rem' }}>
          <div className="stat-card-label">Why This Matters</div>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '0.375rem', lineHeight: 1.6 }}>{finding.explanation_context}</p>
        </div>
      )}

      {/* Prompt Injection Warning */}
      {finding.control_id === "SEC-INJ-001" && (
        <div className="glass-panel" style={{ padding: '1.25rem', marginBottom: '1rem', borderColor: 'var(--error-color)' }}>
          <div className="flex items-center gap-2" style={{ color: 'var(--error-color)', marginBottom: '0.5rem' }}>
            <AlertTriangle size={18} />
            <span style={{ fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Prompt Injection Attempt Detected</span>
          </div>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
            Malicious configuration text attempted to influence the AI processing layer. The AI has <strong>not</strong> evaluated this config. Deterministic findings remain secure.
          </p>
        </div>
      )}

      {/* Remediation Hint */}
      {finding.remediation_hint && !finding.exact_remediation && (
        <div className="glass-panel" style={{ padding: '1rem', marginBottom: '1rem', borderColor: 'rgba(16, 185, 129, 0.2)' }}>
          <div className="stat-card-label" style={{ color: 'var(--success-color)' }}>Deterministic Remediation</div>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '0.375rem' }}>{finding.remediation_hint}</p>
        </div>
      )}

      {/* Exact Remediation */}
      {finding.exact_remediation && (
        <div className="glass-panel" style={{ padding: '1.25rem', marginBottom: '1rem', borderColor: 'rgba(16, 185, 129, 0.4)' }}>
          <div className="stat-card-label" style={{ color: 'var(--success-color)', marginBottom: '0.75rem' }}>Deterministic Remediation Intelligence</div>
          
          <div style={{ marginBottom: '1rem' }}>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Problem Description</div>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '0.25rem' }}>{finding.exact_remediation.problem_description}</p>
          </div>
          
          <div style={{ marginBottom: '1rem' }}>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Remediation Strategy</div>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '0.25rem' }}>{finding.exact_remediation.remediation_explanation}</p>
          </div>
          
          <div style={{ marginBottom: '1rem' }}>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Vendor-Specific CLI ({finding.exact_remediation.vendor.toUpperCase()})</div>
            <pre style={{ fontSize: '0.8rem', background: 'rgba(0,0,0,0.2)', padding: '0.75rem', borderRadius: '4px', marginTop: '0.25rem', color: 'var(--success-color)' }}>{finding.exact_remediation.vendor_cli}</pre>
          </div>
          
          <div className="grid grid-2 gap-3" style={{ marginTop: '1rem', borderTop: '1px solid var(--surface-border)', paddingTop: '1rem' }}>
            <div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Human Approval Required</div>
              <span className="badge" style={{ marginTop: '0.25rem', background: finding.exact_remediation.human_approval_required ? 'rgba(239, 68, 68, 0.1)' : 'rgba(16, 185, 129, 0.1)', color: finding.exact_remediation.human_approval_required ? 'var(--error-color)' : 'var(--success-color)' }}>
                {finding.exact_remediation.human_approval_required ? 'YES' : 'NO'}
              </span>
            </div>
            <div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Safe Guidance</div>
              <p style={{ fontSize: '0.8rem', color: 'var(--warning-color)', marginTop: '0.25rem' }}>{finding.exact_remediation.safe_guidance}</p>
            </div>
          </div>
        </div>
      )}

      {/* AI Section */}
      <div style={{ marginTop: '1.5rem', borderTop: '1px solid var(--surface-border)', paddingTop: '1.5rem' }}>
        <div className="flex items-center gap-2" style={{ marginBottom: '0.75rem' }}>
          <Bot size={16} style={{ color: '#8b5cf6' }} />
          <span style={{ fontSize: '0.75rem', fontWeight: 600, color: '#8b5cf6', textTransform: 'uppercase', letterSpacing: '0.06em' }}>AI-Assisted Interpretation</span>
        </div>

        {!aiResult && !aiLoading && (
          <button className="btn btn-secondary" onClick={requestAI} disabled={aiLoading}>
            <Bot size={16} /> Request AI Explanation
          </button>
        )}

        {aiLoading && (
          <div className="glass-panel" style={{ padding: '1.5rem', textAlign: 'center' }}>
            <Loader size={24} className="animate-spin" style={{ color: '#8b5cf6', marginBottom: '0.5rem' }} />
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Generating AI explanation...</p>
          </div>
        )}

        {aiError && (
          <div className="glass-panel" style={{ padding: '1rem' }}>
            <div className="error-banner" style={{ marginBottom: '0.5rem' }}><AlertTriangle size={16} />{aiError}</div>
            <button className="btn btn-ghost btn-sm" onClick={requestAI}><RefreshCw size={14} /> Retry</button>
          </div>
        )}

        {aiResult && (
          <div className="glass-panel" style={{ padding: '1.25rem', borderColor: 'rgba(139, 92, 246, 0.2)' }}>
            {aiResult.explanation && (
              <div style={{ marginBottom: '1rem' }}>
                <div className="stat-card-label" style={{ color: '#8b5cf6' }}>AI Explanation</div>
                <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: 1.7, marginTop: '0.375rem', whiteSpace: 'pre-wrap' }}>{aiResult.explanation}</div>
              </div>
            )}
            {aiResult.remediation && (
              <div>
                <div className="stat-card-label" style={{ color: '#8b5cf6' }}>AI Remediation</div>
                <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: 1.7, marginTop: '0.375rem', whiteSpace: 'pre-wrap' }}>{aiResult.remediation}</div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
