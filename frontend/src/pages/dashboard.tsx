import { useEffect, useState } from "react";
import { createTicket, listTickets } from "../api/tickets";
import type { Ticket, TicketCreate, TicketStatus } from "../types/ticket";
import { STATUS_OPTIONS, toLabel } from "../utils/status";


export default function Dashboard() {
  // This holds the tickets we got from the backend
  const [tickets, setTickets] = useState<Ticket[]>([]);

  // This controls "Loading..." message
  const [loading, setLoading] = useState(true);

  // This holds error message if something fails
  const [error, setError] = useState<string | null>(null);

  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState<string | null>(null);

  // This holds what the user types in the form
  const [form, setForm] = useState<TicketCreate>({
    title: "",
    message: "",
    status: "open",
  });

  // This function loads tickets from the backend again
  async function refresh() {
    setLoading(true);
    setError(null);
    try {
      const data = await listTickets();  // ask backend: "give me all tickets"
      setTickets(data);                  // save tickets into state
    } catch (e: any) {
      setError(e?.message || "Failed to load tickets"); // show friendly error
    } finally {
      setLoading(false); // stop showing "Loading..."
    }
  }

  // When the page opens, automatically load tickets once
  useEffect(() => {
    refresh();
  }, []);

  // When user clicks "Create" button, this runs
  async function onSubmit(e: React.FormEvent) {
    e.preventDefault(); // stop the browser from reloading the page
    setError(null);
    setSuccess(null);
    setSubmitting(true);

    try {
    await createTicket(form);
    setForm({ title: "", message: "", status: "open" }); // IMPORTANT: API value
    setSuccess("Ticket created ✅");
    await refresh();
  } catch (e: any) {
    setError(e?.message || "Failed to create ticket");
  } finally {
    setSubmitting(false);
  }
}

    return (
    <div style={{ padding: 24, maxWidth: 1000, margin: "0 auto" }}>
      <h1>Dashboard</h1>

      <h2>Create Ticket</h2>

      {/* Purpose: show clean feedback to the user */}
      {success && <p style={{ color: "green" }}>{success}</p>}
      {error && <p style={{ color: "crimson" }}>{error}</p>}

      <form onSubmit={onSubmit} style={{ display: "grid", gap: 10, marginBottom: 24 }}>
        <input
          placeholder="Title"
          value={form.title}
          onChange={(e) => setForm((p) => ({ ...p, title: e.target.value }))}
          required
          disabled={submitting}
        />

        <textarea
          placeholder="Message"
          value={form.message}
          onChange={(e) => setForm((p) => ({ ...p, message: e.target.value }))}
          required
          rows={4}
          disabled={submitting}
        />

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

        <button type="submit" disabled={submitting}>
          {submitting ? "Creating..." : "Create"}
        </button>
      </form>

      <h2>Tickets</h2>
      {loading && <p>Loading...</p>}

      {!loading && tickets.length === 0 && <p>No tickets yet.</p>}

      {!loading && tickets.length > 0 && (
        <table width="100%" cellPadding={10} style={{ borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th align="left">ID</th>
              <th align="left">Title</th>
              <th align="left">Status</th>
              <th align="left">Created</th>
            </tr>
          </thead>

          <tbody>
            {tickets.map((t) => (
              <tr key={t.id} style={{ borderTop: "1px solid #ddd" }}>
                <td>{t.id}</td>
                <td>
                  {/* Note: better with <Link> from react-router-dom, but this works */}
                  <a href={`/tickets/${t.id}`}>{t.title}</a>
                </td>
                <td>{toLabel(t.status)}</td>
                <td>{new Date(t.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}