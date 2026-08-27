// NEXUS — Extended API Service
// Centralized API communication with error handling

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

class ApiError extends Error {
  constructor(message, status, detail) {
    super(message);
    this.status = status;
    this.detail = detail;
  }
}

async function request(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), options.timeout || 30000);
  
  // Setup default headers including authentication
  const headers = new Headers(options.headers || {});
  if (!headers.has('Authorization')) {
    headers.set('Authorization', 'Bearer demo-token-123'); // Demo token required by backend
  }

  try {
    const response = await fetch(url, {
      ...options,
      headers,
      signal: controller.signal,
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new ApiError(
        errorData.detail || `Request failed with status ${response.status}`,
        response.status,
        errorData
      );
    }
    
    return response.json();
  } catch (err) {
    if (err.name === 'AbortError') {
      throw new ApiError('Request timed out', 408, null);
    }
    if (err instanceof ApiError) throw err;
    throw new ApiError(
      err.message || 'Network error — backend may be unavailable',
      0,
      null
    );
  } finally {
    clearTimeout(timeout);
  }
}

// === Scan Operations ===

export async function uploadConfiguration(file) {
  const formData = new FormData();
  formData.append('file', file);
  return request('/scans/upload', {
    method: 'POST',
    body: formData,
  });
}

export async function scanRawConfig(rawConfig, vendorHint = null) {
  return request('/scans/scan', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ raw_config: rawConfig, vendor_hint: vendorHint }),
  });
}

export async function listScans() {
  return request('/scans/');
}

export async function getScanDetail(scanId) {
  return request(`/scans/${scanId}`);
}

export async function getScanGraph(scanId) {
  return request(`/scans/${scanId}/graph`);
}

export function getCsvExportUrl(scanId) {
  return `${API_BASE_URL}/scans/${scanId}/export/csv`;
}

// === AI Operations ===

export async function explainFinding(finding, devicePlatform, rawConfigEvidence) {
  return request('/ai/explain', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      finding,
      device_platform: devicePlatform || 'unknown',
      raw_config_evidence: rawConfigEvidence || '',
    }),
    timeout: 60000, // AI calls can take longer
  });
}

export async function sendChatMessage(scanId, question) {
  return request('/ai/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ scan_id: scanId, question }),
    timeout: 60000,
  });
}

// === System Operations ===

export async function checkHealth() {
  return request('/health', { timeout: 5000 });
}

export { ApiError };
