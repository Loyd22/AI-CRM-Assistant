import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { getTicket } from "../api/tickets";
import { analyzeTicket, type AIAnalysisResult } from "../api/ai";
import type { Ticket } from "../types/ticket";
import { toLabel } from "../utils/status";

function formatDate(isoDate: string) {
  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit",
  }).format(new Date(isoDate));
}

function urgencyBadgeClass(urgency: string) {
  const normalized = urgency.toLowerCase();
  if (normalized.includes("high") || normalized.includes("critical")) {
    return "status-pill status-pill-critical";
  }
  if (normalized.includes("medium")) return "status-pill status-pill-progress";
  return "status-pill status-pill-open";
}

function statusPillClass(status: Ticket["status"]) {
  if (status === "resolved") return "status-pill status-pill-resolved";
  if (status === "in_progress") return "status-pill status-pill-progress";
  return "status-pill status-pill-open";
}

export default function TicketDetail() {
  const { id } = useParams();
  const ticketId = Number(id);
  const invalidId = Number.isNaN(ticketId) || ticketId <= 0;

  const [ticket, setTicket] = useState<Ticket | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [ai, setAi] = useState<AIAnalysisResult | null>(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiError, setAiError] = useState<string | null>(null);

  useEffect(() => {
    async function run() {
      setLoading(true);
      setError(null);
      try {
        const data = await getTicket(ticketId);
        setTicket(data);
      } catch (e: any) {
        setError(e?.message || "Failed to load ticket");
      } finally {
        setLoading(false);
      }
    }
    if (!invalidId) {
      run();
      return;
    }
    setLoading(false);
    setError("Invalid ticket id.");
  }, [invalidId, ticketId]);

  async function onAnalyze() {
    if (!ticket) return;
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
    <div className="crm-app">
      <header className="crm-topbar">
        <div>
          <p className="section-kicker">Ticket Workspace</p>
          <h1>Ticket Detail</h1>
          <p className="section-subtitle">
            Review context and generate AI recommendations before responding.
          </p>
        </div>
        <Link className="btn btn-secondary" to="/">
          Back to Dashboard
        </Link>
      </header>

      {error && <div className="alert alert-danger">{error}</div>}

      {loading && (
        <div className="detail-grid">
          <article className="panel state-block">
            <div className="skeleton-row" />
            <div className="skeleton-row" />
            <div className="skeleton-row" />
            <div className="skeleton-row" />
          </article>
          <article className="panel state-block">
            <div className="skeleton-row" />
            <div className="skeleton-row" />
            <div className="skeleton-row" />
          </article>
        </div>
      )}

      {!loading && ticket && (
        <div className="detail-grid">
          <article className="panel">
            <div className="panel-header">
              <div>
                <h2>{ticket.title}</h2>
                <p>Ticket #{ticket.id}</p>
              </div>
              <span className={statusPillClass(ticket.status)}>{toLabel(ticket.status)}</span>
            </div>

            <div className="meta-row">
              <div className="meta-chip">
                <span className="meta-label">Created</span>
                <strong>{formatDate(ticket.created_at)}</strong>
              </div>
              <div className="meta-chip">
                <span className="meta-label">Last Updated</span>
                <strong>{formatDate(ticket.updated_at)}</strong>
              </div>
            </div>

            <div className="ticket-message">
              <h3>Customer Message</h3>
              <p>{ticket.message}</p>
            </div>
          </article>

          <article className="panel ai-panel">
            <div className="panel-header">
              <div>
                <h2>AI Analysis</h2>
                <p>Generate classification, urgency, and next-step guidance.</p>
              </div>
            </div>

            <button className="btn" onClick={onAnalyze} disabled={aiLoading || invalidId}>
              {aiLoading ? "Analyzing Ticket..." : "Analyze Ticket"}
            </button>

            {aiError && <div className="alert alert-danger">{aiError}</div>}

            {!ai && !aiLoading && (
              <div className="state-block empty-block">
                <p>Run analysis to generate a recommended response package.</p>
              </div>
            )}

            {aiLoading && (
              <div className="state-block">
                <div className="skeleton-row" />
                <div className="skeleton-row" />
                <div className="skeleton-row" />
                <div className="skeleton-row" />
              </div>
            )}

            {ai && !aiLoading && (
              <div className="ai-results">
                <div className="ai-summary">
                  <h3>Summary</h3>
                  <p>{ai.summary}</p>
                </div>

                <div className="ai-grid">
                  <div className="ai-metric">
                    <span>Category</span>
                    <strong>{ai.category}</strong>
                  </div>
                  <div className="ai-metric">
                    <span>Urgency</span>
                    <strong className={urgencyBadgeClass(ai.urgency)}>{ai.urgency}</strong>
                  </div>
                  <div className="ai-metric">
                    <span>Suggested Action</span>
                    <strong>{ai.suggested_action}</strong>
                  </div>
                </div>

                <div className="draft-block">
                  <h3>Draft Reply</h3>
                  <pre className="draft-pre">{ai.draft_reply}</pre>
                </div>
              </div>
            )}
          </article>
        </div>
      )}
    </div>
  );
}
