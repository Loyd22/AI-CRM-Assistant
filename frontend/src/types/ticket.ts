// This limits status to only these 3 exact words.
// So you don't accidentally use a wrong status like "Done".
export type TicketStatus = "open" | "in Progress" | "resolved";

// This describes what a full Ticket looks like when backend sends it back.
// Think: "this is the ticket object shape we will display in the UI".
export type Ticket = {
  id: number;              // ticket unique number created by the database
  title: string;           // ticket title
  message: string;         // ticket message/details
  status: TicketStatus;    // must be Open/In Progress/Resolved
  category?: string | null;    // optional extra info (can be empty)
  urgency?: string | null;     // optional extra info (can be empty)
  assigned_to?: string | null; // optional extra info (can be empty)
  created_at: string;      // when it was created (from backend)
  updated_at: string;      // when it was last updated (from backend)
};

// This describes what we send when we create a new ticket.
// Notice: no id, created_at, updated_at because backend will generate them.
export type TicketCreate = {
  title: string;               // required
  message: string;             // required
  status?: TicketStatus;       // optional (if not sent, backend can default)
  category?: string | null;    // optional
  urgency?: string | null;     // optional
  assigned_to?: string | null; // optional
};