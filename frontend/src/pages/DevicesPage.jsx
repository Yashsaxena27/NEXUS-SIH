import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Server, ScanLine } from 'lucide-react';
import { listScans } from '../services/api';
import { VENDORS } from '../utils/constants';
import { formatDate, formatScore, getScoreColor, getRiskLevel } from '../utils/formatters';

export default function DevicesPage() {
  const navigate = useNavigate();
  const [devices, setDevices] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    listScans().then(scans => {
      const deviceMap = {};
      scans.forEach(s => {
        const key = (s.hostname || 'unknown') + '|' + s.vendor;
        if (!deviceMap[key] || new Date(s.created_at) > new Date(deviceMap[key].created_at)) {
          deviceMap[key] = s;
        }
      });
      setDevices(Object.values(deviceMap));
    }).catch(() => setDevices([])).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading-state"><div className="loading-spinner" /></div>;

  if (!devices?.length) {
    return (
      <div className="empty-state animate-fade-in">
        <div className="empty-state-icon"><Server size={48} /></div>
        <div className="empty-state-title">No Devices Detected</div>
        <div className="empty-state-description">Devices are automatically discovered when you scan configurations.</div>
        <button className="btn btn-primary" onClick={() => navigate('/scan/new')}><ScanLine size={16} /> Scan a Device</button>
      </div>
    );
  }

  return (
    <div className="animate-fade-in">
      <div className="page-header"><h2>Devices & Assets</h2><p>{devices.length} device{devices.length !== 1 ? 's' : ''} discovered</p></div>
      <div className="grid grid-auto">
        {devices.map((d, i) => {
          const rl = getRiskLevel(d.risk_score);
          const v = VENDORS[d.vendor] || VENDORS.unknown;
          return (
            <div key={i} className="glass-panel glass-panel-hover animate-fade-in-up" style={{ padding: '1.25rem', cursor: 'pointer', animationDelay: `${i * 0.05}s`, opacity: 0 }} onClick={() => navigate(`/scan/${d.scan_id}`)}>
              <div className="flex items-center gap-3" style={{ marginBottom: '0.75rem' }}>
                <div style={{ width: 40, height: 40, borderRadius: 8, background: v.color + '20', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Server size={20} style={{ color: v.color }} />
                </div>
                <div>
                  <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>{d.hostname || 'Unknown Host'}</div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{v.label} • {d.platform || ''}</div>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Last scan: {formatDate(d.created_at)}</span>
                <div className="flex items-center gap-2">
                  <span style={{ fontWeight: 600, color: getScoreColor(d.compliance_score) }}>{formatScore(d.compliance_score)}</span>
                  <span style={{ fontSize: '0.7rem', color: rl.color }}>{rl.label}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
