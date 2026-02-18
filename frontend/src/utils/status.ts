// frontend/src/utils/status.ts
// Purpose: Central mapping between UI labels and backend API status values.

import type { TicketStatus, TicketStatusLabel } from "../types/ticket";

export const STATUS_OPTIONS: Array<{ label: TicketStatusLabel; value: TicketStatus }> = [
  { label: "Open", value: "open" },
  { label: "In Progress", value: "in_progress" },
  { label: "Resolved", value: "resolved" },
];

// Optional helpers
export function toLabel(value: TicketStatus): TicketStatusLabel {
  const found = STATUS_OPTIONS.find((s) => s.value === value);
  return found ? found.label : "Open";
}