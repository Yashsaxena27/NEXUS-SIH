import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { LogOut, User } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { checkHealth } from '../../services/api';

const PAGE_TITLES = {
  '/dashboard': 'Security Overview',
  '/scan/new': 'New Security Scan',
  '/scan/result': 'Scan Results',
  '/findings': 'Security Findings',
  '/devices': 'Devices & Assets',
  '/history': 'Scan History',
  '/compare': 'Scan Comparison',
  '/compliance': 'Compliance Coverage',
  '/reports': 'Security Reports',
  '/settings': 'Settings',
};

export default function TopBar() {
  const { user, logout } = useAuth();
  const location = useLocation();
  const [health, setHealth] = useState(null);

  const title = PAGE_TITLES[location.pathname] || 'NEXUS';

  useEffect(() => {
    checkHealth().then(setHealth).catch(() => setHealth(null));
  }, []);

  return (
    <header className="topbar">
      <h2 className="topbar-title">{title}</h2>
      <div className="topbar-actions">
        <div className="flex items-center gap-2" style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
          <span className={`health-dot ${health ? 'online' : 'offline'}`} />
          {health ? 'Engine Online' : 'Checking...'}
        </div>
        {health && !health.ai_available && (
          <span className="badge badge-warning" style={{ fontSize: '0.6rem' }}>AI Unavailable</span>
        )}
        <div className="flex items-center gap-2" style={{ borderLeft: '1px solid var(--surface-border)', paddingLeft: '1rem' }}>
          <User size={16} style={{ color: 'var(--text-secondary)' }} />
          <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{user?.name || 'User'}</span>
          <button className="btn btn-ghost btn-sm" onClick={logout} aria-label="Logout" title="Logout">
            <LogOut size={16} />
          </button>
        </div>
      </div>
    </header>
  );
}
