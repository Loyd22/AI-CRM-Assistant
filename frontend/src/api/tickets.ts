// Import the generic "call the backend" helper
import { apiFetch } from "./http";

// Import ticket types so TypeScript knows the shape of data
import type { Ticket, TicketCreate } from "../types/ticket";

// Get the list of all tickets from the backend
export function listTickets() {
  // Calls backend: GET /api/v1/tickets
  // Returns: a list of tickets
  return apiFetch<Ticket[]>("/api/v1/tickets");
}

// Get one ticket by its id
export function getTicket(id: number) {
  // Calls backend: GET /api/v1/tickets/{id}
  // Returns: one ticket
  return apiFetch<Ticket>(`/api/v1/tickets/${id}`);
}

// Create a new ticket in the backend
export function createTicket(payload: TicketCreate) {
  // Calls backend: POST /api/v1/tickets
  // Sends ticket data as JSON
  // Returns: the created ticket (with id and timestamps)
  return apiFetch<Ticket>("/api/v1/tickets", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}