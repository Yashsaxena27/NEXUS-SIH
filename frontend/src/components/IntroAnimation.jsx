import React, { useState, useEffect } from 'react';
import { Shield } from 'lucide-react';

const WORDS = ['NETWORK', 'ANALYZE', 'VERIFY', 'SECURE'];
const WORD_DELAY = 500;
const TOTAL_DURATION = WORD_DELAY * WORDS.length + 1200;

export default function IntroAnimation({ onComplete }) {
  const [visibleWords, setVisibleWords] = useState(0);
  const [fading, setFading] = useState(false);

  useEffect(() => {
    const timers = [];
    WORDS.forEach((_, i) => {
      timers.push(setTimeout(() => setVisibleWords(i + 1), WORD_DELAY * (i + 1) + 600));
    });
    timers.push(setTimeout(() => setFading(true), TOTAL_DURATION - 400));
    timers.push(setTimeout(onComplete, TOTAL_DURATION));
    return () => timers.forEach(clearTimeout);
  }, [onComplete]);

  return (
    <div className="intro-screen" style={{ opacity: fading ? 0 : 1, transition: 'opacity 0.4s ease' }}>
      <div className="intro-content">
        <div style={{ marginBottom: '1.5rem', animation: 'fadeInUp 0.5s ease forwards' }}>
          <div style={{ background: 'var(--accent-gradient)', width: 56, height: 56, borderRadius: 12, display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1rem' }}>
            <Shield size={32} color="white" />
          </div>
          <div className="intro-logo">NEXUS</div>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', alignItems: 'center' }}>
          {WORDS.map((word, i) => (
            <div key={word} className="intro-word" style={{
              animationDelay: `${0.6 + i * 0.5}s`,
              color: i < visibleWords ? 'var(--accent-color)' : 'var(--text-muted)',
              transition: 'color 0.3s ease',
            }}>
              {word}
            </div>
          ))}
        </div>
      </div>
      <button className="btn btn-ghost intro-skip" onClick={onComplete} aria-label="Skip intro">
        Skip →
      </button>
    </div>
  );
}
