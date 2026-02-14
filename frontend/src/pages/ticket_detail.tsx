import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getTicket } from "../api/tickets";
import { analyzeTicket, type AIAnalyzeResult } from "../api/ai";
import type { Ticket } from "../types/ticket";

export default function TicketDetail() {
  const { id } = useParams();
  const ticketId = Number(id);

  const [ticket, setTicket] = useState<Ticket | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [ai, setAi] = useState<AIAnalyzeResult | null>(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiError, setAiError] = useState<string | null>(null);

  useEffect(() => {
    async function run() {
      setError(null);
      try {
        const data = await getTicket(ticketId);
        setTicket(data);
      } catch (e: any) {
        setError(e?.message || "Failed to load ticket");
      }
    }
    if (!Number.isNaN(ticketId)) run();
  }, [ticketId]);

  async function onAnalyze() {
    setAiLoading(true);
    setAiError(null);
    try {
      const result = await analyzeTicket(ticketId);
      setAi(result);
    } catch (e: any) {
      setAiError(e?.message || "Failed to analyze ticket");
    } finally {
      setAiLoading(false);
    }
  }

  return (
    <div style={{ padding: 24, maxWidth: 900, margin: "0 auto" }}>
      <Link to="/">← Back</Link>

      {error && <p style={{ color: "crimson" }}>{error}</p>}
      {!ticket && !error && <p>Loading...</p>}

      {ticket && (
        <>
          <h1>{ticket.title}</h1>
          <p><b>Status:</b> {ticket.status}</p>

          <p><b>Message:</b></p>
          <pre style={{ whiteSpace: "pre-wrap" }}>{ticket.message}</pre>

          <hr style={{ margin: "20px 0" }} />

          <button onClick={onAnalyze} disabled={aiLoading}>
            {aiLoading ? "Analyzing..." : "Analyze"}
          </button>

          {aiError && <p style={{ color: "crimson" }}>{aiError}</p>}

          {ai && (
            <div style={{ marginTop: 16 }}>
              <h2>AI Result</h2>
              <p><b>Summary:</b> {ai.summary}</p>
              <p><b>Category:</b> {ai.category}</p>
              <p><b>Urgency:</b> {ai.urgency}</p>
              <p><b>Suggested action:</b> {ai.suggested_action}</p>
              <p><b>Draft reply:</b></p>
              <pre style={{ whiteSpace: "pre-wrap" }}>{ai.draft_reply}</pre>
            </div>
          )}
        </>
      )}
    </div>
  );
}