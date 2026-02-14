// This page shows 1 ticket details, based on the URL like /tickets/5

import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getTicket } from "../api/tickets";
import type { Ticket } from "../types/ticket";

export default function TicketDetail() {
  // Read the ticket id from the URL (example: /tickets/5 => id = "5")
  const { id } = useParams();

  // Convert id to number so we can use it in API call
  const ticketId = Number(id);

  // Store the ticket data we get from backend
  const [ticket, setTicket] = useState<Ticket | null>(null);

  // Store error message if something fails
  const [error, setError] = useState<string | null>(null);

  // When the page opens (or when ticketId changes), load the ticket
  useEffect(() => {
    async function run() {
      setError(null);
      try {
        const data = await getTicket(ticketId); // ask backend: "give me ticket by id"
        setTicket(data);                        // save it for display
      } catch (e: any) {
        setError(e?.message || "Failed to load ticket");
      }
    }

    // Only run if ticketId is a valid number
    if (!Number.isNaN(ticketId)) run();
  }, [ticketId]);

  return (
    <div style={{ padding: 24, maxWidth: 900, margin: "0 auto" }}>
      {/* Simple back link */}
      <a href="/">← Back</a>

      {error && <p style={{ color: "crimson" }}>{error}</p>}
      {!ticket && !error && <p>Loading...</p>}

      {/* When ticket exists, show details */}
      {ticket && (
        <>
          <h1>{ticket.title}</h1>
          <p><b>Status:</b> {ticket.status}</p>
          <p><b>Message:</b></p>

          {/* Show message with line breaks */}
          <pre style={{ whiteSpace: "pre-wrap" }}>{ticket.message}</pre>
        </>
      )}
    </div>
  );
}