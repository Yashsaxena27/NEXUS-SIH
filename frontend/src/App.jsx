import React, { useState, useCallback } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ScanProvider } from './context/ScanContext';
import AppShell from './components/Layout/AppShell';
import IntroAnimation from './components/IntroAnimation';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import NewScanPage from './pages/NewScanPage';
import ScanResultPage from './pages/ScanResultPage';
import FindingsPage from './pages/FindingsPage';
import FindingDetailPage from './pages/FindingDetailPage';
import ScanHistoryPage from './pages/ScanHistoryPage';
import ScanComparePage from './pages/ScanComparePage';
import DevicesPage from './pages/DevicesPage';
import CompliancePage from './pages/CompliancePage';
import ReportsPage from './pages/ReportsPage';
import SettingsPage from './pages/SettingsPage';
import './index.css';

function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();
  if (loading) return <div className="loading-state"><div className="loading-spinner" /></div>;
  return isAuthenticated ? children : <Navigate to="/login" replace />;
}

function AppContent() {
  const [showIntro, setShowIntro] = useState(() => !sessionStorage.getItem('nexus_intro_done'));
  const { isAuthenticated } = useAuth();

  const handleIntroComplete = useCallback(() => {
    setShowIntro(false);
    sessionStorage.setItem('nexus_intro_done', '1');
  }, []);

  if (showIntro && !isAuthenticated) {
    return <IntroAnimation onComplete={handleIntroComplete} />;
  }

  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/" element={<ProtectedRoute><AppShell /></ProtectedRoute>}>
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<DashboardPage />} />
        <Route path="scan/new" element={<NewScanPage />} />
        <Route path="scan/result" element={<ScanResultPage />} />
        <Route path="scan/:scanId" element={<ScanResultPage />} />
        <Route path="findings" element={<FindingsPage />} />
        <Route path="findings/:controlId" element={<FindingDetailPage />} />
        <Route path="history" element={<ScanHistoryPage />} />
        <Route path="compare" element={<ScanComparePage />} />
        <Route path="devices" element={<DevicesPage />} />
        <Route path="compliance" element={<CompliancePage />} />
        <Route path="reports" element={<ReportsPage />} />
        <Route path="settings" element={<SettingsPage />} />
      </Route>
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <ScanProvider>
          <AppContent />
        </ScanProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}
