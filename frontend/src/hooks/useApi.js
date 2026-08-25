import { useState, useCallback } from 'react';

/**
 * Hook for API calls with loading, error, and data state management.
 * Usage:
 *   const { data, loading, error, execute } = useApi(api.listScans);
 *   // Then call execute() when ready
 */
export function useApi(apiFn) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const execute = useCallback(async (...args) => {
    setLoading(true);
    setError(null);
    try {
      const result = await apiFn(...args);
      setData(result);
      return result;
    } catch (err) {
      setError(err.message || 'An unexpected error occurred');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [apiFn]);

  const reset = useCallback(() => {
    setData(null);
    setLoading(false);
    setError(null);
  }, []);

  return { data, loading, error, execute, reset };
}
