import React from 'react';
import { Shield } from 'lucide-react';

export default function Header() {
  return (
    <header className="flex justify-between items-center" style={{ marginBottom: '3rem' }}>
      <div className="flex items-center gap-2">
        <div style={{ background: 'var(--accent-gradient)', padding: '0.5rem', borderRadius: '0.5rem' }}>
          <Shield size={28} color="white" />
        </div>
        <div>
          <h1 className="gradient-text" style={{ fontSize: '1.5rem', margin: 0 }}>NEXUS</h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', margin: 0 }}>
            Network Security Compliance Auditor
          </p>
        </div>
      </div>
    </header>
  );
}
