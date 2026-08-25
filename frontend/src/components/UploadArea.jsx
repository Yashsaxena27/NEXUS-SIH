import React from 'react';
import { UploadCloud, AlertTriangle, RefreshCw } from 'lucide-react';

export default function UploadArea({ file, onFileChange, onDrop, error, scanning, onScan }) {
  return (
    <div className="glass-panel animate-fade-in" style={{ padding: '3rem', maxWidth: '800px', margin: '0 auto' }}>
      <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '2rem', marginBottom: '1rem' }}>Upload Configuration</h2>
        <p style={{ color: 'var(--text-secondary)' }}>
          Scan your network configuration files (Cisco, Fortinet, Palo Alto, Juniper) for compliance against security baselines.
        </p>
      </div>
      
      <div 
        className="drop-zone"
        onDragOver={(e) => e.preventDefault()}
        onDrop={onDrop}
        onClick={() => document.getElementById('file-upload').click()}
      >
        <input 
          id="file-upload" 
          type="file" 
          style={{ display: 'none' }} 
          onChange={onFileChange} 
        />
        <UploadCloud size={48} color="var(--accent-color)" style={{ marginBottom: '1rem' }} />
        {file ? (
          <h3 style={{ color: 'var(--text-primary)' }}>{file.name} ({Math.round(file.size / 1024)} KB)</h3>
        ) : (
          <>
            <h3 style={{ color: 'var(--text-primary)', marginBottom: '0.5rem' }}>Drag & drop your config file here</h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>or click to browse</p>
          </>
        )}
      </div>
      
      {error && (
        <div style={{ marginTop: '1.5rem', padding: '1rem', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid var(--error-color)', borderRadius: '0.5rem', color: 'var(--error-color)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <AlertTriangle size={20} />
          {error}
        </div>
      )}

      <div style={{ marginTop: '2rem', textAlign: 'center' }}>
        <button 
          className="btn btn-primary" 
          style={{ fontSize: '1rem', padding: '0.75rem 3rem' }}
          disabled={!file || scanning}
          onClick={onScan}
        >
          {scanning ? (
            <><RefreshCw className="spin" size={20} style={{ animation: 'spin 1s linear infinite' }} /> Analyzing...</>
          ) : (
            <>Analyze Configuration</>
          )}
        </button>
      </div>
    </div>
  );
}
