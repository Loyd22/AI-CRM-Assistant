import { useEffect, useState } from "react";
import { createTicket, listTickets } from "../api/tickets";
import type { Ticket, TicketCreate, TicketStatus } from "../types/ticket";

export default function Dashboard() {
  // This holds the tickets we got from the backend
  const [tickets, setTickets] = useState<Ticket[]>([]);

  // This controls "Loading..." message
  const [loading, setLoading] = useState(true);

  // This holds error message if something fails
  const [error, setError] = useState<string | null>(null);

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
    try {
      await createTicket(form); // send the form data to backend to create a ticket
      setForm({ title: "", message: "", status: "open" }); // clear the form
      await refresh(); // reload ticket list so the new ticket appears
    } catch (e: any) {
      setError(e?.message || "Failed to create ticket");
    }
  }

  return (
    <div style={{ padding: 24, maxWidth: 1000, margin: "0 auto" }}>
      <h1>Dashboard</h1>

      <h2>Create Ticket</h2>

      {/* This is the form where the user types ticket title/message/status */}
      <form onSubmit={onSubmit} style={{ display: "grid", gap: 10, marginBottom: 24 }}>
        <input
          placeholder="Title"
          value={form.title}
          // When user types, update form.title
          onChange={(e) => setForm((p) => ({ ...p, title: e.target.value }))}
          required
        />

        <textarea
          placeholder="Message"
          value={form.message}
          // When user types, update form.message
          onChange={(e) => setForm((p) => ({ ...p, message: e.target.value }))}
          required
          rows={4}
        />

        <select
          value={form.status || "open"}
          // When user changes status, update form.status
          onChange={(e) => setForm((p) => ({ ...p, status: e.target.value as TicketStatus }))}
        >
          <option value="open">Open</option>
          <option value="in_progress">In Progress</option>
          <option value="resolved">Resolved</option>
        </select>

        <button type="submit">Create</button>
      </form>

      <h2>Tickets</h2>

      {/* Show loading message while waiting for backend */}
      {loading && <p>Loading...</p>}

      {/* Show error message if something failed */}
      {error && <p style={{ color: "crimson" }}>{error}</p>}

      {/* If loaded but no tickets exist */}
      {!loading && tickets.length === 0 && <p>No tickets yet.</p>}

      {/* If tickets exist, show table */}
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

                {/* Clicking title goes to ticket detail page */}
                <td>
                  <a href={`/tickets/${t.id}`}>{t.title}</a>
                </td>

                <td>{t.status}</td>

                {/* Convert created_at (string) into readable date */}
                <td>{new Date(t.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}