import { apiFetch } from "./http";

export type AIAnalyzeResult = {
  summary: string;
  category: string;
  urgency: string;
  suggested_action: string;
  draft_reply: string;
};

export function analyzeTicket(ticketId: number) {
  return apiFetch<AIAnalyzeResult>(`/api/v1/tickets/${ticketId}/analyze`, {
    method: "POST",
  });
}