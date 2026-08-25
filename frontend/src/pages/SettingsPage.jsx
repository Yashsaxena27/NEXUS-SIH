import React, { useEffect, useState } from 'react';
import { Settings as SettingsIcon, Activity, Bot, Database, Globe, LogOut, User } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { checkHealth } from '../services/api';
import { formatDate } from '../utils/formatters';

export default function SettingsPage() {
  const { user, logout } = useAuth();
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    checkHealth()
      .then(setHealth)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  const StatusRow = ({ icon: Icon, label, status, ok }) => (
    <div className="flex items-center gap-3" style={{ padding: '0.75rem 0', borderBottom: '1px solid var(--surface-border)' }}>
      <Icon size={18} style={{ color: ok ? 'var(--success-color)' : 'var(--error-color)' }} />
      <span style={{ flex: 1, fontSize: '0.85rem' }}>{label}</span>
      <span className="flex items-center gap-2">
        <span className={`health-dot ${ok ? 'online' : 'offline'}`} />
        <span style={{ fontSize: '0.8rem', color: ok ? 'var(--success-color)' : 'var(--error-color)', fontWeight: 500 }}>{status}</span>
      </span>
    </div>
  );

  return (
    <div className="animate-fade-in" style={{ maxWidth: 700, margin: '0 auto' }}>
      <div className="page-header"><h2>Settings</h2></div>

      {/* System Health */}
      <div className="glass-panel" style={{ padding: '1.25rem', marginBottom: '1rem' }}>
        <h3 style={{ fontSize: '1rem', marginBottom: '0.75rem' }}>System Health</h3>
        {loading && <div className="loading-state" style={{ padding: '1rem' }}><div className="loading-spinner" /></div>}
        {error && <div className="error-banner" style={{ marginBottom: 0 }}><Activity size={16} /> Backend unavailable: {error}</div>}
        {health && (
          <div>
            <StatusRow icon={Activity} label="NEXUS Engine" status="Online" ok={true} />
            <StatusRow icon={Database} label="Database" status={health.database === 'connected' ? 'Connected' : 'Disconnected'} ok={health.database === 'connected'} />
            <StatusRow icon={Bot} label="AI Service (Gemini)" status={health.ai_available ? 'Available' : 'Unavailable'} ok={health.ai_available} />
          </div>
        )}
        {!loading && !health && !error && (
          <StatusRow icon={Activity} label="NEXUS Engine" status="Offline" ok={false} />
        )}
      </div>

      {/* Application Info */}
      <div className="glass-panel" style={{ padding: '1.25rem', marginBottom: '1rem' }}>
        <h3 style={{ fontSize: '1rem', marginBottom: '0.75rem' }}>Application</h3>
        <div className="flex justify-between" style={{ padding: '0.5rem 0', fontSize: '0.85rem' }}>
          <span style={{ color: 'var(--text-secondary)' }}>Version</span>
          <span>{health?.version || '—'}</span>
        </div>
        <div className="flex justify-between" style={{ padding: '0.5rem 0', fontSize: '0.85rem', borderTop: '1px solid var(--surface-border)' }}>
          <span style={{ color: 'var(--text-secondary)' }}>API Endpoint</span>
          <span style={{ fontFamily: 'monospace', fontSize: '0.8rem' }}>{import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'}</span>
        </div>
        <div className="flex justify-between" style={{ padding: '0.5rem 0', fontSize: '0.85rem', borderTop: '1px solid var(--surface-border)' }}>
          <span style={{ color: 'var(--text-secondary)' }}>Supported Vendors</span>
          <span>Cisco, Juniper, Fortinet, Palo Alto</span>
        </div>
      </div>

      {/* Profile */}
      <div className="glass-panel" style={{ padding: '1.25rem' }}>
        <h3 style={{ fontSize: '1rem', marginBottom: '0.75rem' }}>Profile</h3>
        <div className="flex items-center gap-3" style={{ marginBottom: '1rem' }}>
          <div style={{ width: 40, height: 40, borderRadius: '50%', background: 'var(--accent-gradient)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <User size={20} color="white" />
          </div>
          <div>
            <div style={{ fontWeight: 600 }}>{user?.name || 'Unknown'}</div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{user?.role || 'User'} • Logged in {user?.loginTime ? formatDate(user.loginTime) : ''}</div>
          </div>
        </div>
        <button className="btn btn-secondary w-full" onClick={logout}>
          <LogOut size={16} /> Sign Out
        </button>
      </div>
    </div>
  );
}
