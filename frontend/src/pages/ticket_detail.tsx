// Purpose: Ticket detail page UI.
// Fits in: src/pages. Shows ticket and triggers AI analyze.
// Inputs: URL param :id
// Outputs: Renders ticket info + AI analysis panel.

import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getTicket } from "../api/tickets";
import { analyzeTicket, type AIAnalysisResult } from "../api/ai";
import type { Ticket } from "../types/ticket";
import { toLabel } from "../utils/status";


export default function TicketDetail() {
  const { id } = useParams();
  const ticketId = Number(id);

  const [ticket, setTicket] = useState<Ticket | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [ai, setAi] = useState<AIAnalysisResult | null>(null);
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
    setAiError(null);
    setAiLoading(true);
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
      <a href="/">← Back</a>

      {error && <p style={{ color: "crimson" }}>{error}</p>}
      {!ticket && !error && <p>Loading...</p>}

      {ticket && (
        <>
          <h1>{ticket.title}</h1>
          <p><b>Status:</b> {toLabel(ticket.status)}</p>

          <p><b>Message:</b></p>
          <pre style={{ whiteSpace: "pre-wrap" }}>{ticket.message}</pre>

          <hr style={{ margin: "24px 0" }} />

          <h2>AI Analysis</h2>

          <button onClick={onAnalyze} disabled={aiLoading}>
            {aiLoading ? "Analyzing..." : "Analyze"}
          </button>

          {aiError && <p style={{ color: "crimson" }}>{aiError}</p>}

          {!ai && !aiLoading && <p>No AI analysis yet. Click Analyze.</p>}

          {ai && (
            <div style={{ marginTop: 16, padding: 16, border: "1px solid #ddd" }}>
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