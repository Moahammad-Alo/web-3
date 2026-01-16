/**
 * API service for making fetch requests to the Django backend.
 * Handles CSRF tokens and JSON parsing.
 */

import type { ApiError } from '@/types';

/**
 * Get the CSRF token from cookies.
 */
function getCsrfToken(): string {
  const cookie = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='));
  return cookie ? cookie.split('=')[1] : '';
}

/**
 * Base API request function with CSRF handling.
 */
export async function apiRequest<T>(
  url: string,
  options: RequestInit = {}
): Promise<T> {
  const defaultHeaders: HeadersInit = {
    'X-CSRFToken': getCsrfToken(),
  };

  // Only add Content-Type for JSON requests (not for FormData)
  if (!(options.body instanceof FormData)) {
    defaultHeaders['Content-Type'] = 'application/json';
  }

  const response = await fetch(url, {
    credentials: 'include',
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  });

  if (!response.ok) {
    let errorMessage = `API Error: ${response.status}`;
    try {
      const errorData: ApiError = await response.json();
      errorMessage = errorData.error || errorMessage;
    } catch {
      // Ignore JSON parse errors
    }
    throw new Error(errorMessage);
  }

  return response.json();
}

/**
 * GET request helper.
 */
export async function get<T>(url: string): Promise<T> {
  return apiRequest<T>(url, { method: 'GET' });
}

/**
 * POST request helper.
 */
export async function post<T>(url: string, data: unknown): Promise<T> {
  const body = data instanceof FormData ? data : JSON.stringify(data);
  return apiRequest<T>(url, { method: 'POST', body });
}

/**
 * PUT request helper.
 */
export async function put<T>(url: string, data: unknown): Promise<T> {
  const body = data instanceof FormData ? data : JSON.stringify(data);
  return apiRequest<T>(url, { method: 'PUT', body });
}

/**
 * DELETE request helper.
 */
export async function del<T>(url: string): Promise<T> {
  return apiRequest<T>(url, { method: 'DELETE' });
}
