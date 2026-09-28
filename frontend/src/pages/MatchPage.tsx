import { useState } from 'react';
import { AppShell } from '../components/AppShell';
import { matchCandidates } from '../services/api';
import type { CandidateMatch } from '../types/api';

export function MatchPage() {
  const [jd, setJd] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [candidates, setCandidates] = useState<CandidateMatch[]>([]);

  async function handleAnalyze() {
    setError(null);
    if (!jd.trim()) {
      setError('Cole um Job Description antes de analisar.');
      return;
    }
    setLoading(true);
    setCandidates([]);
    try {
      const result = await matchCandidates({ job_description: jd.trim() });
      setCandidates(result.candidates);
      if (result.candidates.length === 0) {
        setError('Nenhum candidato encontrado. Indexe currículos na aba Indexação.');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Falha na análise.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <AppShell>
      <div className="page-panel">
        <h1 className="display display--sm">Curadoria de talentos</h1>
        <p className="lede">
          Cole o Job Description e receba o Top 3 com justificativa consultiva.
        </p>

        <label className="field">
          <span>Job Description</span>
          <textarea
            rows={10}
            value={jd}
            disabled={loading}
            onChange={(e) => setJd(e.target.value)}
            placeholder="Cole aqui a descrição da vaga…"
          />
        </label>

        <button
          type="button"
          className="btn btn--primary"
          disabled={loading}
          onClick={handleAnalyze}
        >
          {loading ? 'Analisando…' : 'Analisar candidatos'}
        </button>

        {error ? <p className="banner banner--error">{error}</p> : null}

        {candidates.length > 0 ? (
          <section className="results">
            <h2>Top 3 candidatos</h2>
            {candidates
              .slice()
              .sort((a, b) => a.rank - b.rank)
              .map((c) => (
                <article key={`${c.rank}-${c.name}`} className="candidate">
                  <header>
                    <span className="rank">#{c.rank}</span>
                    <h3>{c.name}</h3>
                  </header>
                  <p>{c.justification}</p>
                </article>
              ))}
          </section>
        ) : null}
      </div>
    </AppShell>
  );
}
