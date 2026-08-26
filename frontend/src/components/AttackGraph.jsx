import React, { useEffect, useState } from 'react';
import { getScanGraph } from '../services/api';
import { Network, AlertTriangle, ShieldAlert, Globe } from 'lucide-react';
import { SEVERITY_CONFIG } from '../utils/constants';

export default function AttackGraph({ scanId }) {
  const [graph, setGraph] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!scanId) return;
    setLoading(true);
    getScanGraph(scanId)
      .then(d => setGraph(d))
      .catch(e => console.error(e))
      .finally(() => setLoading(false));
  }, [scanId]);

  if (loading) return <div style={{ padding: '1rem', color: 'var(--text-muted)' }}>Loading attack graph...</div>;
  if (!graph || graph.nodes.length === 0) return null;

  const externalNodes = graph.nodes.filter(n => n.type === 'EXTERNAL');
  const assetNodes = graph.nodes.filter(n => n.type === 'ASSET');
  const findingNodes = graph.nodes.filter(n => n.type === 'FINDING');
  const vulnNodes = graph.nodes.filter(n => n.type === 'VULNERABILITY');

  const getNodeIcon = (type) => {
    if (type === 'EXTERNAL') return <Globe size={18} />;
    if (type === 'ASSET') return <Network size={18} />;
    if (type === 'FINDING') return <AlertTriangle size={18} />;
    if (type === 'VULNERABILITY') return <ShieldAlert size={18} />;
    return <Network size={18} />;
  };

  const getNodeColor = (node) => {
    if (node.type === 'EXTERNAL') return 'var(--info-color)';
    if (node.type === 'ASSET') return 'var(--text-primary)';
    if (node.severity) return SEVERITY_CONFIG[node.severity]?.color || 'var(--warning-color)';
    return 'var(--warning-color)';
  };

  return (
    <div className="glass-panel" style={{ padding: '1.25rem', marginBottom: '1.5rem', overflowX: 'auto' }}>
      <div className="stat-card-label" style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <Network size={16} style={{ color: 'var(--accent-color)' }} /> Attack Path / Exposure Graph
      </div>
      
      <div style={{ display: 'flex', alignItems: 'center', gap: '2rem', minWidth: '600px', padding: '1rem 0' }}>
        {/* Layer 1: External */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {externalNodes.map(n => (
            <div key={n.id} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.75rem', background: 'rgba(255,255,255,0.05)', border: `1px solid ${getNodeColor(n)}`, borderRadius: '6px' }}>
              <div style={{ color: getNodeColor(n) }}>{getNodeIcon(n.type)}</div>
              <span style={{ fontSize: '0.85rem', fontWeight: 600 }}>{n.label}</span>
            </div>
          ))}
        </div>
        
        <div style={{ height: '2px', background: 'var(--surface-border)', width: '30px' }} />

        {/* Layer 2: Asset */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {assetNodes.map(n => (
            <div key={n.id} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.75rem', background: 'rgba(255,255,255,0.05)', border: `1px solid ${getNodeColor(n)}`, borderRadius: '6px' }}>
              <div style={{ color: getNodeColor(n) }}>{getNodeIcon(n.type)}</div>
              <span style={{ fontSize: '0.85rem', fontWeight: 600 }}>{n.label}</span>
            </div>
          ))}
        </div>

        <div style={{ height: '2px', background: 'var(--surface-border)', width: '30px' }} />
        
        {/* Layer 3: Findings & Vulns */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {findingNodes.map(n => (
            <div key={n.id} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.75rem', background: 'rgba(255,255,255,0.05)', border: `1px solid ${getNodeColor(n)}`, borderRadius: '6px' }}>
              <div style={{ color: getNodeColor(n) }}>{getNodeIcon(n.type)}</div>
              <span style={{ fontSize: '0.85rem', fontWeight: 600 }}>{n.id}: {n.label.length > 25 ? n.label.substring(0, 25) + '...' : n.label}</span>
            </div>
          ))}
          {vulnNodes.map(n => (
            <div key={n.id} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.75rem', background: 'rgba(255,255,255,0.05)', border: `1px solid ${getNodeColor(n)}`, borderRadius: '6px' }}>
              <div style={{ color: getNodeColor(n) }}>{getNodeIcon(n.type)}</div>
              <span style={{ fontSize: '0.85rem', fontWeight: 600 }}>{n.id}</span>
            </div>
          ))}
        </div>
      </div>
      
      <div style={{ marginTop: '0.5rem', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
        This graph represents logical exposure points. Edges are inferred from deterministic scan data.
      </div>
    </div>
  );
}
