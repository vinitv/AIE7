/**
 * Configuration for API endpoints
 */

// Get the API base URL based on environment
export const getApiBaseUrl = (): string => {
  // For unified service, API and frontend are served from the same domain
  // In development, still use localhost:8000 for separate services
  if (typeof window !== 'undefined') {
    // In browser - check if we're in development
    if (window.location.hostname === 'localhost' && window.location.port !== '8000') {
      // Development mode with separate frontend/backend
      return 'http://localhost:8000';
    } else {
      // Production or unified service - API on same domain
      return window.location.origin;
    }
  }
  
  // Server-side rendering fallback
  return '';
};

export const API_ENDPOINTS = {
  TEST_KEYS: '/api/test-keys',
  ASK: '/ask',
  HEALTH: '/health',
} as const; 