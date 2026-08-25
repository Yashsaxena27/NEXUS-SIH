import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, FileText, CheckCircle, Loader, AlertTriangle, X } from 'lucide-react';
import { uploadConfiguration } from '../services/api';
import { useScan } from '../context/ScanContext';
import { formatFileSize } from '../utils/formatters';

const STAGES = [
  'Uploading configuration...',
  'Detecting vendor...',
  'Parsing configuration...',
  'Normalizing to security IR...',
  'Evaluating compliance controls...',
  'Building security posture...',
  'Complete',
];

export default function NewScanPage() {
  const navigate = useNavigate();
  const { setScanResult } = useScan();
  const [file, setFile] = useState(null);
  const [scanName, setScanName] = useState('');
  const [scanning, setScanning] = useState(false);
  const [currentStage, setCurrentStage] = useState(-1);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const inputRef = useRef();

  const handleDrop = (e) => {
    e.preventDefault();
    setDragActive(false);
    if (e.dataTransfer.files?.[0]) { setFile(e.dataTransfer.files[0]); setError(null); }
  };

  const handleFileChange = (e) => {
    if (e.target.files?.[0]) { setFile(e.target.files[0]); setError(null); }
  };

  const handleScan = async () => {
    if (!file) return;
    setScanning(true);
    setError(null);
    setCurrentStage(0);

    // Progress stages run on timers (deterministic UX, not fake percentages)
    const stageTimers = [];
    for (let i = 1; i < STAGES.length - 1; i++) {
      stageTimers.push(setTimeout(() => setCurrentStage(i), i * 350));
    }

    try {
      const result = await uploadConfiguration(file);
      stageTimers.forEach(clearTimeout);
      setCurrentStage(STAGES.length - 1); // Complete
      setScanResult(result);
      setTimeout(() => navigate('/scan/result'), 600);
    } catch (err) {
      stageTimers.forEach(clearTimeout);
      setError(err.message);
      setScanning(false);
      setCurrentStage(-1);
    }
  };

  return (
    <div className="animate-fade-in" style={{ maxWidth: 640, margin: '0 auto' }}>
      <div className="page-header text-center">
        <h2>New Security Scan</h2>
        <p>Upload a network device configuration for compliance analysis</p>
      </div>

      {!scanning ? (
        <div className="glass-panel" style={{ padding: '2rem' }}>
          <div
            className={`drop-zone${dragActive ? ' active' : ''}`}
            onClick={() => inputRef.current?.click()}
            onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
            onDragLeave={() => setDragActive(false)}
            onDrop={handleDrop}
            role="button"
            tabIndex={0}
            aria-label="Upload configuration file"
            onKeyDown={(e) => e.key === 'Enter' && inputRef.current?.click()}
          >
            <input ref={inputRef} type="file" style={{ display: 'none' }} onChange={handleFileChange} accept=".cfg,.conf,.txt,.config,.log" />
            <Upload size={32} style={{ color: 'var(--text-muted)', marginBottom: '0.75rem' }} />
            <p style={{ color: 'var(--text-primary)', fontWeight: 500, marginBottom: '0.25rem' }}>
              {file ? file.name : 'Drop configuration file here or click to browse'}
            </p>
            {file ? (
              <div className="flex items-center justify-center gap-2" style={{ marginTop: '0.5rem' }}>
                <FileText size={14} style={{ color: 'var(--accent-color)' }} />
                <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{formatFileSize(file.size)}</span>
                <button className="btn btn-ghost btn-sm" onClick={(e) => { e.stopPropagation(); setFile(null); }} aria-label="Remove file"><X size={14} /></button>
              </div>
            ) : (
              <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                Supported: Cisco IOS/IOS-XE, Juniper Junos, Fortinet FortiOS, Palo Alto PAN-OS
              </p>
            )}
          </div>

          <div style={{ marginTop: '1.25rem' }}>
            <label className="input-label">Scan Name (optional)</label>
            <input className="input" placeholder="e.g., Core Router Audit" value={scanName} onChange={e => setScanName(e.target.value)} />
          </div>

          {error && (
            <div className="error-banner" style={{ marginTop: '1rem', marginBottom: 0 }}>
              <AlertTriangle size={16} />{error}
            </div>
          )}

          <button className="btn btn-primary btn-lg w-full" style={{ marginTop: '1.25rem' }} onClick={handleScan} disabled={!file}>
            <ScanIcon size={18} /> Analyze Configuration
          </button>
        </div>
      ) : (
        <div className="glass-panel" style={{ padding: '2rem' }}>
          <h3 style={{ marginBottom: '1.5rem', textAlign: 'center' }}>Analyzing Configuration</h3>
          <div className="scan-stages">
            {STAGES.map((label, i) => (
              <div key={i} className="scan-stage">
                <div className={`scan-stage-dot ${i < currentStage ? 'complete' : i === currentStage ? 'active' : 'pending'}`}>
                  {i < currentStage ? <CheckCircle size={14} color="white" /> : i === currentStage ? <Loader size={14} color="white" className="animate-spin" /> : null}
                </div>
                <span className={`scan-stage-label ${i < currentStage ? 'complete' : i === currentStage ? 'active' : ''}`}>{label}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function ScanIcon(props) { return <svg {...props} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 7V5a2 2 0 012-2h2"/><path d="M17 3h2a2 2 0 012 2v2"/><path d="M21 17v2a2 2 0 01-2 2h-2"/><path d="M7 21H5a2 2 0 01-2-2v-2"/><line x1="7" y1="12" x2="17" y2="12"/></svg>; }
