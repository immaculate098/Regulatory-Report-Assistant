import { useEffect, useMemo, useState } from 'react';
import './App.css';
import axios from 'axios';
import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

const API_BASE = (import.meta?.env?.VITE_API_BASE || process.env.REACT_APP_API_BASE || 'https://regulatory-report-assistant.onrender.com').replace(/\/$/, '');

function App() {
  const [input, setInput] = useState('Patient experienced severe nausea and headache after taking Drug X. Patient recovered.');
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [translating, setTranslating] = useState(false);
  const [translated, setTranslated] = useState(null);

  useEffect(() => {
    axios.get(`${API_BASE}/reports`)
      .then(res => setHistory(res.data))
      .catch(() => {});
  }, []);

  const onProcess = async () => {
    setProcessing(true);
    setTranslated(null);
    try {
      const res = await axios.post(`${API_BASE}/process-report`, { report: input });
      setResult(res.data);
      // refresh history
      const rep = await axios.get(`${API_BASE}/reports`);
      setHistory(rep.data);
    } catch (e) {
      alert('Failed to process report');
    } finally {
      setProcessing(false);
    }
  };

  const onTranslate = async (language) => {
    if (!result?.outcome) return;
    setTranslating(true);
    try {
      const res = await axios.post(`${API_BASE}/translate`, { outcome: result.outcome, language });
      setTranslated(res.data.translated);
    } catch (e) {
      alert('Translation failed');
    } finally {
      setTranslating(false);
    }
  };

  const severityChart = useMemo(() => {
    const counts = { mild: 0, moderate: 0, severe: 0 };
    history.forEach(h => {
      if (h.severity && counts.hasOwnProperty(h.severity)) counts[h.severity] += 1;
    });
    return {
      labels: ['Mild', 'Moderate', 'Severe'],
      datasets: [
        {
          data: [counts.mild, counts.moderate, counts.severe],
          backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
          borderWidth: 0,
        }
      ]
    };
  }, [history]);

  const severityClass = (sev) => sev ? `pill severity-${sev}` : 'pill';

  return (
    <div className="container">
      <div className="header">
        <div className="brand">Regulatory Report Assistant</div>
      </div>

      <div className="grid">
        <div className="card">
          <div className="muted" style={{marginBottom: 8}}>Paste medical report</div>
          <textarea value={input} onChange={e => setInput(e.target.value)} placeholder="Enter report text..." />
          <div className="controls">
            <button onClick={onProcess} disabled={processing}>{processing ? 'Processing...' : 'Process Report'}</button>
            <button className="secondary" onClick={() => setInput('')} disabled={processing}>Clear</button>
          </div>
        </div>

        <div className="card">
          <div className="muted" style={{marginBottom: 8}}>Extraction Result</div>
          {result ? (
            <table className="table">
              <tbody>
                <tr><th>Drug</th><td>{result.drug || '-'}</td></tr>
                <tr><th>Adverse Events</th><td>{(result.adverse_events||[]).join(', ') || '-'}</td></tr>
                <tr><th>Severity</th><td><span className={severityClass(result.severity)}>{result.severity || '-'}</span></td></tr>
                <tr><th>Outcome</th><td>{result.outcome || '-'}</td></tr>
              </tbody>
            </table>
          ) : (
            <div className="muted">No result yet.</div>
          )}
          <div className="controls" style={{marginTop: 12}}>
            <button onClick={() => onTranslate('fr')} disabled={!result?.outcome || translating}>Translate to French</button>
            <button onClick={() => onTranslate('sw')} disabled={!result?.outcome || translating}>Translate to Swahili</button>
            {translated && <span className="pill">{translated}</span>}
          </div>
        </div>
      </div>

      <div className="grid" style={{marginTop: 18}}>
        <div className="card">
          <div className="muted" style={{marginBottom: 8}}>History</div>
          <table className="table">
            <thead><tr><th>When</th><th>Drug</th><th>Events</th><th>Severity</th><th>Outcome</th></tr></thead>
            <tbody>
              {history.map(h => (
                <tr key={h.id}>
                  <td className="muted">{new Date(h.created_at).toLocaleString()}</td>
                  <td>{h.drug || '-'}</td>
                  <td>{(h.adverse_events||[]).join(', ')}</td>
                  <td><span className={severityClass(h.severity)}>{h.severity || '-'}</span></td>
                  <td>{h.outcome || '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="card">
          <div className="muted" style={{marginBottom: 8}}>Severity Distribution</div>
          <Doughnut data={severityChart} />
        </div>
      </div>
    </div>
  );
}

export default App;
