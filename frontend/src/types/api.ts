export interface MatchRequest {
  job_description: string;
}

export interface CandidateMatch {
  rank: number;
  name: string;
  justification: string;
}

export interface MatchResponse {
  candidates: CandidateMatch[];
}

export interface IndexedItem {
  filename: string;
  name: string;
  point_id: string;
}

export interface IndexResponse {
  indexed_count: number;
  items: IndexedItem[];
}
