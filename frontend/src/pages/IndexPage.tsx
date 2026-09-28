import { useState } from 'react';
import { AppShell } from '../components/AppShell';
import { indexFiles } from '../services/api';

export function IndexPage() {
  const [files, setFiles] = useState<File[]>([]);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  function onSelect(fileList: FileList | null) {
    setSuccess(null);
    setError(null);
    if (!fileList) {
      setFiles([]);
      return;
    }
    const selected = Array.from(fileList).filter((f) =>
      f.name.toLowerCase().endsWith('.txt'),
    );
    if (selected.length === 0) {
      setFiles([]);
      setError('Selecione apenas arquivos .txt.');
      return;
    }
    setFiles(selected);
  }

  async function handleIndex() {
    setSuccess(null);
    setError(null);
    if (files.length === 0) {
      setError('Selecione ao menos um arquivo .txt.');
      return;
    }
    setLoading(true);
    try {
      const result = await indexFiles(files);
      setSuccess(
        `${result.indexed_count} arquivo(s) indexado(s) com sucesso.`,
      );
      setFiles([]);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Falha na indexação. Tente novamente.',
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <AppShell>
      <div className="page-panel">
        <h1 className="display display--sm">Indexação</h1>
        <p className="lede">
          Envie um ou mais currículos em `.txt`. Cada arquivo vira um único
          documento no Qdrant (sem chunking).
        </p>

        <label className="upload">
          <span className="upload__label">Arquivos .txt</span>
          <input
            type="file"
            accept=".txt,text/plain"
            multiple
            disabled={loading}
            onChange={(e) => onSelect(e.target.files)}
          />
        </label>

        {files.length > 0 ? (
          <ul className="file-list">
            {files.map((file) => (
              <li key={`${file.name}-${file.size}`}>
                {file.name}{' '}
                <span className="muted">({Math.round(file.size / 1024)} KB)</span>
              </li>
            ))}
          </ul>
        ) : null}

        <button
          type="button"
          className="btn btn--primary"
          disabled={loading}
          onClick={handleIndex}
        >
          {loading ? 'Indexando…' : 'Indexar'}
        </button>

        {success ? <p className="banner banner--success">{success}</p> : null}
        {error ? <p className="banner banner--error">{error}</p> : null}
      </div>
    </AppShell>
  );
}
