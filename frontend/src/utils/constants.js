// NEXUS Design System — Constants
// Centralized colors, labels, and configuration

export const SEVERITY_CONFIG = {
  CRITICAL: { color: '#ef4444', bg: 'rgba(239, 68, 68, 0.1)', border: 'rgba(239, 68, 68, 0.2)', label: 'Critical', icon: '🔴' },
  HIGH:     { color: '#f97316', bg: 'rgba(249, 115, 22, 0.1)', border: 'rgba(249, 115, 22, 0.2)', label: 'High', icon: '🟠' },
  MEDIUM:   { color: '#f59e0b', bg: 'rgba(245, 158, 11, 0.1)', border: 'rgba(245, 158, 11, 0.2)', label: 'Medium', icon: '🟡' },
  LOW:      { color: '#3b82f6', bg: 'rgba(59, 130, 246, 0.1)', border: 'rgba(59, 130, 246, 0.2)', label: 'Low', icon: '🔵' },
  INFORMATIONAL: { color: '#6b7280', bg: 'rgba(107, 114, 128, 0.1)', border: 'rgba(107, 114, 128, 0.2)', label: 'Info', icon: '⚪' },
};

export const STATUS_CONFIG = {
  PASS:                 { color: '#10b981', bg: 'rgba(16, 185, 129, 0.1)', border: 'rgba(16, 185, 129, 0.2)', label: 'Pass' },
  FAIL:                 { color: '#ef4444', bg: 'rgba(239, 68, 68, 0.1)', border: 'rgba(239, 68, 68, 0.2)', label: 'Fail' },
  UNKNOWN:              { color: '#f59e0b', bg: 'rgba(245, 158, 11, 0.1)', border: 'rgba(245, 158, 11, 0.2)', label: 'Unknown' },
  UNKNOWN_ABSENT:       { color: '#f59e0b', bg: 'rgba(245, 158, 11, 0.1)', border: 'rgba(245, 158, 11, 0.2)', label: 'Not Present' },
  UNKNOWN_PARSE_ERROR:  { color: '#8b5cf6', bg: 'rgba(139, 92, 246, 0.1)', border: 'rgba(139, 92, 246, 0.2)', label: 'Parse Error' },
};

export const STATUS_DESCRIPTIONS = {
  PASS: 'Control requirement is met',
  FAIL: 'Control requirement is not met',
  UNKNOWN_ABSENT: 'Expected configuration field not present in device config',
  UNKNOWN_PARSE_ERROR: 'Configuration could not be safely parsed for this control',
};

export const RISK_LEVELS = [
  { max: 20, label: 'Low', color: '#10b981' },
  { max: 50, label: 'Medium', color: '#f59e0b' },
  { max: 80, label: 'High', color: '#f97316' },
  { max: Infinity, label: 'Critical', color: '#ef4444' },
];

export const NAV_ITEMS = [
  { id: 'dashboard', label: 'Overview', icon: 'LayoutDashboard', path: '/dashboard' },
  { id: 'new-scan', label: 'New Scan', icon: 'ScanLine', path: '/scan/new' },
  { id: 'findings', label: 'Findings', icon: 'ShieldAlert', path: '/findings' },
  { id: 'devices', label: 'Devices', icon: 'Server', path: '/devices' },
  { id: 'history', label: 'Scan History', icon: 'History', path: '/history' },
  { id: 'compare', label: 'Compare', icon: 'GitCompare', path: '/compare' },
  { id: 'compliance', label: 'Compliance', icon: 'ClipboardCheck', path: '/compliance' },
  { id: 'reports', label: 'Reports', icon: 'FileText', path: '/reports' },
  { id: 'settings', label: 'Settings', icon: 'Settings', path: '/settings' },
];

export const VENDORS = {
  cisco: { label: 'Cisco IOS/IOS-XE', color: '#049fd9' },
  juniper: { label: 'Juniper Junos', color: '#84b135' },
  fortinet: { label: 'Fortinet FortiOS', color: '#ee3124' },
  paloalto: { label: 'Palo Alto PAN-OS', color: '#fa582d' },
  unknown: { label: 'Unknown Vendor', color: '#6b7280' },
};
