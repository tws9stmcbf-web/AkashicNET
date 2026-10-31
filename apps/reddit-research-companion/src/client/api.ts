import type { Session } from '../shared/model.js';

export const request = async <T>(path: string, body?: unknown): Promise<T> => {
  const response = await fetch(path, body === undefined ? undefined : {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body),
  });
  if (!response.ok) {
    const failure: { error?: string } = await response.json();
    throw new Error(failure.error ?? 'The request could not be completed.');
  }
  return response.json();
};

export const loadSession = () => request<Session>('/api/session');
