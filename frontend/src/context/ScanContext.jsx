import React, { createContext, useContext, useState, useCallback } from 'react';

const ScanContext = createContext(null);

export function ScanProvider({ children }) {
  const [currentScan, setCurrentScan] = useState(null);
  const [scanHistory, setScanHistory] = useState([]);
  const [selectedFinding, setSelectedFinding] = useState(null);

  const setScanResult = useCallback((result) => {
    setCurrentScan(result);
    if (result) {
      setScanHistory(prev => {
        const exists = prev.find(s => s.scan_id === result.scan_id);
        if (exists) return prev;
        return [result, ...prev];
      });
    }
  }, []);

  const clearCurrentScan = useCallback(() => {
    setCurrentScan(null);
    setSelectedFinding(null);
  }, []);

  return (
    <ScanContext.Provider value={{
      currentScan,
      setScanResult,
      clearCurrentScan,
      scanHistory,
      setScanHistory,
      selectedFinding,
      setSelectedFinding,
    }}>
      {children}
    </ScanContext.Provider>
  );
}

export function useScan() {
  const ctx = useContext(ScanContext);
  if (!ctx) throw new Error('useScan must be used within ScanProvider');
  return ctx;
}
