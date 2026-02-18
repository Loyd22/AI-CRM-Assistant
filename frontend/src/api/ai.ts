// Purpose: Frontend client for AI analysis endpoints.
// Fits in: src/api layer. Called by pages/components.
// Inputs: ticketId number.
// Outputs: AI analysis JSON from backend.

import { apiFetch } from "./http";

export type AIAnalysisResult = {
  summary: string;
  category: string;
  urgency: string;
  suggested_action: string;
  draft_reply: string;
};

export function analyzeTicket(ticketId: number) {
  return apiFetch<AIAnalysisResult>(`/api/v1/tickets/${ticketId}/analyze`, {
    method: "POST",
  });
}