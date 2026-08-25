import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

const DEMO_USER = { username: 'admin', name: 'NEXUS Admin', role: 'Administrator' };
const SESSION_KEY = 'nexus_session';

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Restore session from localStorage
    const stored = localStorage.getItem(SESSION_KEY);
    if (stored) {
      try {
        setUser(JSON.parse(stored));
      } catch { /* ignore corrupt data */ }
    }
    setLoading(false);
  }, []);

  const login = (username, password) => {
    // Demo authentication — modular for future real auth
    if (username === 'admin' && password === 'nexus2026') {
      const session = { ...DEMO_USER, loginTime: new Date().toISOString() };
      setUser(session);
      localStorage.setItem(SESSION_KEY, JSON.stringify(session));
      return { success: true };
    }
    // Also allow demo access
    if (username === 'demo' && password === 'demo') {
      const session = { username: 'demo', name: 'Demo User', role: 'Viewer', loginTime: new Date().toISOString() };
      setUser(session);
      localStorage.setItem(SESSION_KEY, JSON.stringify(session));
      return { success: true };
    }
    return { success: false, error: 'Invalid credentials' };
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem(SESSION_KEY);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
