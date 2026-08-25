import React, { useState } from 'react';
import { Shield, Lock } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    // Simulate brief delay for UX
    setTimeout(() => {
      const result = login(username, password);
      if (result.success) {
        navigate('/dashboard');
      } else {
        setError(result.error);
      }
      setLoading(false);
    }, 300);
  };

  const fillDemo = () => {
    setUsername('admin');
    setPassword('nexus2026');
    setError('');
  };

  return (
    <div className="login-screen">
      <div className="login-card glass-panel animate-fade-in-up">
        <div className="login-logo">
          <div style={{ background: 'var(--accent-gradient)', width: 48, height: 48, borderRadius: 10, display: 'inline-flex', alignItems: 'center', justifyContent: 'center', marginBottom: '0.75rem' }}>
            <Shield size={26} color="white" />
          </div>
          <h1 className="gradient-text" style={{ fontSize: '1.75rem', marginBottom: '0.25rem' }}>NEXUS</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>Network Security Compliance Auditor</p>
        </div>

        <form className="login-form" onSubmit={handleSubmit}>
          <div style={{ textAlign: 'center', marginBottom: '0.5rem' }}>
            <Lock size={14} style={{ color: 'var(--text-muted)', verticalAlign: 'middle', marginRight: 4 }} />
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Secure access to your security posture</span>
          </div>

          {error && <div className="login-error">{error}</div>}

          <div className="input-group">
            <label className="input-label" htmlFor="username">Username</label>
            <input id="username" className="input" type="text" placeholder="Enter username" value={username} onChange={(e) => setUsername(e.target.value)} autoComplete="username" required autoFocus />
          </div>

          <div className="input-group">
            <label className="input-label" htmlFor="password">Password</label>
            <input id="password" className="input" type="password" placeholder="Enter password" value={password} onChange={(e) => setPassword(e.target.value)} autoComplete="current-password" required />
          </div>

          <label className="login-remember">
            <input type="checkbox" defaultChecked /> Remember me
          </label>

          <button className="btn btn-primary btn-lg w-full" type="submit" disabled={loading}>
            {loading ? 'Signing in...' : 'Sign In'}
          </button>

          <div className="login-demo">
            <button type="button" onClick={fillDemo}>Use demo credentials</button>
          </div>
        </form>
      </div>
    </div>
  );
}
