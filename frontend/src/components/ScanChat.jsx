import React, { useState } from 'react';
import { Send, Bot, User, Loader, ShieldAlert } from 'lucide-react';
import { api } from '../services/api';

export default function ScanChat({ scanId }) {
  const [messages, setMessages] = useState([
    { role: 'assistant', text: "Hello! I'm NEXUS. Ask me anything about this scan's findings, risks, or compliance alignment." }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || !scanId) return;
    
    const userMsg = { role: 'user', text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      // Direct fetch using the standard api instance
      const res = await api.post('/ai/chat', { scan_id: scanId, question: userMsg.text });
      setMessages(prev => [...prev, { role: 'assistant', text: res.data.answer }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', text: "Error: " + (err.response?.data?.detail || err.message) }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-panel animate-fade-in-up" style={{ display: 'flex', flexDirection: 'column', height: '400px', marginBottom: '1.5rem' }}>
      <div className="stat-card-label" style={{ padding: '1rem', borderBottom: '1px solid var(--surface-border)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <Bot size={16} style={{ color: '#8b5cf6' }} /> Scan-Aware Security Assistant
      </div>
      
      <div style={{ flex: 1, overflowY: 'auto', padding: '1rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {messages.map((m, i) => (
          <div key={i} style={{ display: 'flex', gap: '0.75rem', flexDirection: m.role === 'user' ? 'row-reverse' : 'row' }}>
            <div style={{ 
              width: 28, height: 28, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center',
              background: m.role === 'user' ? 'rgba(59, 130, 246, 0.2)' : 'rgba(139, 92, 246, 0.2)',
              color: m.role === 'user' ? '#3b82f6' : '#8b5cf6'
            }}>
              {m.role === 'user' ? <User size={14} /> : <Bot size={14} />}
            </div>
            <div style={{ 
              background: m.role === 'user' ? 'rgba(59, 130, 246, 0.1)' : 'rgba(255, 255, 255, 0.03)', 
              padding: '0.75rem', borderRadius: '8px', maxWidth: '80%', fontSize: '0.85rem',
              color: 'var(--text-secondary)', whiteSpace: 'pre-wrap', lineHeight: 1.5,
              border: m.role === 'user' ? '1px solid rgba(59, 130, 246, 0.2)' : '1px solid var(--surface-border)'
            }}>
              {m.text}
            </div>
          </div>
        ))}
        {loading && (
          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <div style={{ width: 28, height: 28, borderRadius: '50%', background: 'rgba(139, 92, 246, 0.2)', color: '#8b5cf6', display: 'flex', alignItems: 'center', justifyContent: 'center' }}><Bot size={14} /></div>
            <div style={{ padding: '0.75rem', borderRadius: '8px', display: 'flex', alignItems: 'center' }}><Loader size={16} className="animate-spin" style={{ color: '#8b5cf6' }} /></div>
          </div>
        )}
      </div>

      <form onSubmit={sendMessage} style={{ padding: '1rem', borderTop: '1px solid var(--surface-border)', display: 'flex', gap: '0.5rem' }}>
        <input 
          type="text" 
          className="input-field" 
          value={input} 
          onChange={e => setInput(e.target.value)} 
          placeholder="Ask about risks, telnet status, CVEs..." 
          disabled={loading}
          style={{ flex: 1 }}
        />
        <button type="submit" className="btn btn-primary" disabled={loading || !input.trim()} style={{ padding: '0 1rem' }}>
          <Send size={16} />
        </button>
      </form>
    </div>
  );
}
