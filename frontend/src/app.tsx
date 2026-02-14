// This decides which page to show based on the URL.

import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/dashboard";
import TicketDetail from "./pages/ticket_detail";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* If URL is "/", show the Dashboard page */}
        <Route path="/" element={<Dashboard />} />

        {/* If URL is "/tickets/123", show TicketDetail page and 123 is the id */}
        <Route path="/tickets/:id" element={<TicketDetail />} />
      </Routes>
    </BrowserRouter>
  );
}