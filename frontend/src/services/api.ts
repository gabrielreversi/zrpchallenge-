import type { IndexResponse, MatchRequest, MatchResponse } from '../types/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000';

async function readError(response: Response): Promise<string> {
  try {
    const data = (await response.json()) as { detail?: string | unknown };
    if (typeof data.detail === 'string') return data.detail;
    return JSON.stringify(data.detail ?? data);
  } catch {
    return `Erro HTTP ${response.status}`;
  }
}

export async function matchCandidates(
  request: MatchRequest,
): Promise<MatchResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/match`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  });
  if (!response.ok) {
    throw new Error(await readError(response));
  }
  return (await response.json()) as MatchResponse;
}

export async function indexFiles(files: File[]): Promise<IndexResponse> {
  const form = new FormData();
  for (const file of files) {
    form.append('files', file);
  }
  const response = await fetch(`${API_BASE_URL}/api/v1/index`, {
    method: 'POST',
    body: form,
  });
  if (!response.ok) {
    throw new Error(await readError(response));
  }
  return (await response.json()) as IndexResponse;
}
