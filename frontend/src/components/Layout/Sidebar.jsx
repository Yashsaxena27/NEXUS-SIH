import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { Shield, LayoutDashboard, ScanLine, ShieldAlert, Server, History, GitCompare, ClipboardCheck, FileText, Settings } from 'lucide-react';

const icons = { LayoutDashboard, ScanLine, ShieldAlert, Server, History, GitCompare, ClipboardCheck, FileText, Settings };

const NAV = [
  { section: 'Analysis', items: [
    { label: 'Overview', icon: 'LayoutDashboard', path: '/dashboard' },
    { label: 'New Scan', icon: 'ScanLine', path: '/scan/new' },
  ]},
  { section: 'Results', items: [
    { label: 'Findings', icon: 'ShieldAlert', path: '/findings' },
    { label: 'Devices', icon: 'Server', path: '/devices' },
    { label: 'Compliance', icon: 'ClipboardCheck', path: '/compliance' },
  ]},
  { section: 'History', items: [
    { label: 'Scan History', icon: 'History', path: '/history' },
    { label: 'Compare', icon: 'GitCompare', path: '/compare' },
    { label: 'Reports', icon: 'FileText', path: '/reports' },
  ]},
  { section: 'System', items: [
    { label: 'Settings', icon: 'Settings', path: '/settings' },
  ]},
];

export default function Sidebar() {
  return (
    <aside className="sidebar" role="navigation" aria-label="Main navigation">
      <div className="sidebar-logo">
        <div className="sidebar-logo-icon">
          <Shield size={20} color="white" />
        </div>
        <div>
          <h1>NEXUS</h1>
          <p>Security Auditor</p>
        </div>
      </div>
      <nav className="sidebar-nav">
        {NAV.map(section => (
          <React.Fragment key={section.section}>
            <div className="sidebar-section-label">{section.section}</div>
            {section.items.map(item => {
              const Icon = icons[item.icon];
              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={({ isActive }) => `sidebar-nav-item${isActive ? ' active' : ''}`}
                  aria-label={item.label}
                >
                  {Icon && <Icon size={18} />}
                  {item.label}
                </NavLink>
              );
            })}
          </React.Fragment>
        ))}
      </nav>
    </aside>
  );
}
