import React, { useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, ScanLine, ShieldAlert } from 'lucide-react';
import { useScan } from '../context/ScanContext';
import { SEVERITY_CONFIG, STATUS_CONFIG } from '../utils/constants';

const STATUS_ORDER = ['FAIL', 'UNKNOWN_ABSENT', 'UNKNOWN_PARSE_ERROR', 'UNKNOWN', 'PASS'];
const SEV_ORDER = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFORMATIONAL'];

export default function FindingsPage() {
  const navigate = useNavigate();
  const { currentScan } = useScan();
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [sevFilter, setSevFilter] = useState('ALL');
  const [search, setSearch] = useState('');

  const findings = currentScan?.findings || [];

  const filtered = useMemo(() => {
    let result = [...findings];
    if (statusFilter !== 'ALL') result = result.filter(f => f.status === statusFilter);
    if (sevFilter !== 'ALL') result = result.filter(f => f.severity === sevFilter);
    if (search.trim()) {
      const q = search.toLowerCase();
      result = result.filter(f =>
        f.control_id?.toLowerCase().includes(q) ||
        f.title?.toLowerCase().includes(q) ||
        (f.control_title || '').toLowerCase().includes(q) ||
        (f.category || '').toLowerCase().includes(q)
      );
    }
    result.sort((a, b) => {
      const si = STATUS_ORDER.indexOf(a.status) - STATUS_ORDER.indexOf(b.status);
      if (si !== 0) return si;
      return SEV_ORDER.indexOf(a.severity) - SEV_ORDER.indexOf(b.severity);
    });
    return result;
  }, [findings, statusFilter, sevFilter, search]);

  if (!currentScan) {
    return (
      <div className="empty-state animate-fade-in">
        <div className="empty-state-icon"><ScanLine size={48} /></div>
        <div className="empty-state-title">No Scan Data Available</div>
        <div className="empty-state-description">Run a security scan first to view findings.</div>
        <button className="btn btn-primary" onClick={() => navigate('/scan/new')}><ScanLine size={16} /> Start Scan</button>
      </div>
    );
  }

  const statusCounts = {};
  findings.forEach(f => { statusCounts[f.status] = (statusCounts[f.status] || 0) + 1; });

  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <h2>Security Findings</h2>
        <p>{findings.length} controls evaluated • {currentScan.vendor} • {currentScan.hostname || 'Unknown Host'}</p>
      </div>

      {/* Summary bar */}
      <div className="flex gap-3" style={{ marginBottom: '1rem', flexWrap: 'wrap' }}>
        {Object.entries(STATUS_CONFIG).map(([key, cfg]) => (
          statusCounts[key] ? (
            <span key={key} className="badge" style={{ background: cfg.bg, color: cfg.color, border: `1px solid ${cfg.border}` }}>
              {cfg.label}: {statusCounts[key]}
            </span>
          ) : null
        ))}
      </div>

      {/* Filters */}
      <div className="flex gap-3 items-center" style={{ marginBottom: '1rem', flexWrap: 'wrap' }}>
        <div className="filter-tabs">
          {['ALL', 'FAIL', 'PASS', 'UNKNOWN_ABSENT'].map(s => (
            <button key={s} className={`filter-tab${statusFilter === s ? ' active' : ''}`} onClick={() => setStatusFilter(s)}>
              {s === 'ALL' ? 'All' : STATUS_CONFIG[s]?.label || s}
            </button>
          ))}
        </div>
        <div className="filter-tabs">
          {['ALL', ...SEV_ORDER.slice(0, 4)].map(s => (
            <button key={s} className={`filter-tab${sevFilter === s ? ' active' : ''}`} onClick={() => setSevFilter(s)}>
              {s === 'ALL' ? 'All' : SEVERITY_CONFIG[s]?.label || s}
            </button>
          ))}
        </div>
        <div className="flex items-center gap-2 flex-1" style={{ minWidth: 200 }}>
          <Search size={16} style={{ color: 'var(--text-muted)' }} />
          <input className="input" placeholder="Search controls..." value={search} onChange={e => setSearch(e.target.value)} style={{ flex: 1 }} />
        </div>
      </div>

      {/* Findings List */}
      <div className="flex flex-col gap-2">
        {filtered.length === 0 && (
          <div className="empty-state" style={{ padding: '2rem' }}>
            <div className="empty-state-title">No findings match your filters</div>
            <button className="btn btn-ghost btn-sm" onClick={() => { setStatusFilter('ALL'); setSevFilter('ALL'); setSearch(''); }}>Clear Filters</button>
          </div>
        )}
        {filtered.map(f => {
          const statusCfg = STATUS_CONFIG[f.status] || STATUS_CONFIG.UNKNOWN;
          const sevCfg = SEVERITY_CONFIG[f.severity] || SEVERITY_CONFIG.LOW;
          return (
            <div key={f.control_id} className="finding-row" onClick={() => navigate(`/findings/${f.control_id}`)}>
              <div className="finding-row-status" style={{ background: statusCfg.color }} />
              <div className="finding-row-content">
                <div className="finding-row-id">{f.control_id}</div>
                <div className="finding-row-title">{f.title || f.control_title}</div>
              </div>
              <div className="finding-row-meta">
                <span className="badge" style={{ background: statusCfg.bg, color: statusCfg.color, border: `1px solid ${statusCfg.border}` }}>{statusCfg.label}</span>
                <span className="badge" style={{ background: sevCfg.bg, color: sevCfg.color, border: `1px solid ${sevCfg.border}` }}>{sevCfg.label}</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
