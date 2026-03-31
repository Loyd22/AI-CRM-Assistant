import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { createTicket, listTickets } from "../api/tickets";
import type { Ticket, TicketCreate, TicketStatus } from "../types/ticket";
import { STATUS_OPTIONS, toLabel } from "../utils/status";

function formatDate(isoDate: string) {
  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit",
  }).format(new Date(isoDate));
}

function statusPillClass(status: TicketStatus) {
  if (status === "resolved") return "status-pill status-pill-resolved";
  if (status === "in_progress") return "status-pill status-pill-progress";
  return "status-pill status-pill-open";
}

export default function Dashboard() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState<string | null>(null);
  const [form, setForm] = useState<TicketCreate>({
    title: "",
    message: "",
    status: "open",
  });

  async function refresh() {
    setLoading(true);
    setError(null);
    try {
      const data = await listTickets();
      setTickets(data);
    } catch (e: any) {
      setError(e?.message || "Failed to load tickets");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refresh();
  }, []);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setSuccess(null);
    setSubmitting(true);

    try {
      await createTicket(form);
      setForm({ title: "", message: "", status: "open" });
      setSuccess("Ticket created and added to the queue.");
      await refresh();
    } catch (e: any) {
      setError(e?.message || "Failed to create ticket");
    } finally {
      setSubmitting(false);
    }
  }

  const metrics = useMemo(() => {
    const open = tickets.filter((ticket) => ticket.status === "open").length;
    const inProgress = tickets.filter(
      (ticket) => ticket.status === "in_progress",
    ).length;
    const resolved = tickets.filter((ticket) => ticket.status === "resolved").length;

    return [
      { label: "Total Tickets", value: tickets.length },
      { label: "Open", value: open },
      { label: "In Progress", value: inProgress },
      { label: "Resolved", value: resolved },
    ];
  }, [tickets]);

  return (
    <div className="crm-app">
      <header className="crm-topbar">
        <div>
          <p className="section-kicker">Portfolio Product Demo</p>
          <h1>AI CRM Assistant</h1>
          <p className="section-subtitle">
            Manage inbound support tickets and escalate action with AI-generated
            recommendations.
          </p>
        </div>
        <button className="btn btn-secondary" onClick={refresh} disabled={loading}>
          {loading ? "Refreshing..." : "Refresh Data"}
        </button>
      </header>

      <section className="stats-grid">
        {metrics.map((metric, index) => (
          <article className="stat-card" key={metric.label} style={{ animationDelay: `${80 * index}ms` }}>
            <span className="stat-label">{metric.label}</span>
            <strong className="stat-value">{metric.value}</strong>
          </article>
        ))}
      </section>

      <section className="content-grid">
        <article className="panel">
          <div className="panel-header">
            <div>
              <h2>Create Ticket</h2>
              <p>Capture a new support issue for the team workflow.</p>
            </div>
          </div>

          {success && <div className="alert alert-success">{success}</div>}

          <form className="ticket-form" onSubmit={onSubmit}>
            <div className="field-grid field-grid-two">
              <label>
                Ticket title
                <input
                  placeholder="Login issue with SSO account"
                  value={form.title}
                  onChange={(e) => setForm((p) => ({ ...p, title: e.target.value }))}
                  required
                  disabled={submitting}
                />
              </label>

              <label>
                Initial status
                <select
                  value={form.status || "open"}
                  onChange={(e) =>
                    setForm((p) => ({ ...p, status: e.target.value as TicketStatus }))
                  }
                  disabled={submitting}
                >
                  {STATUS_OPTIONS.map((opt) => (
                    <option key={opt.value} value={opt.value}>
                      {opt.label}
                    </option>
                  ))}
                </select>
              </label>
            </div>

            <label>
              Message
              <textarea
                placeholder="Describe the issue details and business impact..."
                value={form.message}
                onChange={(e) => setForm((p) => ({ ...p, message: e.target.value }))}
                required
                rows={5}
                disabled={submitting}
              />
            </label>

            <button className="btn" type="submit" disabled={submitting}>
              {submitting ? "Creating Ticket..." : "Create Ticket"}
            </button>
          </form>
        </article>

        <article className="panel table-panel">
          <div className="panel-header">
            <div>
              <h2>Ticket Queue</h2>
              <p>Track active demand across customer accounts.</p>
            </div>
            {!loading && <span className="panel-meta">{tickets.length} records</span>}
          </div>

          {error && (
            <div className="alert alert-danger">
              <span>{error}</span>
              <button className="btn btn-ghost" onClick={refresh}>
                Retry
              </button>
            </div>
          )}

          {loading && (
            <div className="state-block">
              {Array.from({ length: 5 }).map((_, index) => (
                <div className="skeleton-row" key={index} />
              ))}
            </div>
          )}

          {!loading && tickets.length === 0 && (
            <div className="state-block empty-block">
              <p>No tickets yet. Create your first ticket to populate the queue.</p>
            </div>
          )}

          {!loading && tickets.length > 0 && (
            <div className="table-wrap">
              <table className="crm-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Status</th>
                    <th>Created</th>
                    <th />
                  </tr>
                </thead>
                <tbody>
                  {tickets.map((ticket) => (
                    <tr key={ticket.id}>
                      <td>#{ticket.id}</td>
                      <td>
                        <strong>{ticket.title}</strong>
                      </td>
                      <td>
                        <span className={statusPillClass(ticket.status)}>
                          {toLabel(ticket.status)}
                        </span>
                      </td>
                      <td>{formatDate(ticket.created_at)}</td>
                      <td>
                        <Link className="row-link" to={`/tickets/${ticket.id}`}>
                          View
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </article>
      </section>
    </div>
  );
}
