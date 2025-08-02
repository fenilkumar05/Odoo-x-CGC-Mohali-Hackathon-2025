import { tickets } from "@/lib/data";
import { DashboardClient } from "@/components/dashboard/dashboard-client";

export default function DashboardPage() {
  // In a real app, you would fetch this data from an API
  const initialTickets = tickets;

  return (
    <div className="space-y-6">
      <DashboardClient initialTickets={initialTickets} />
    </div>
  );
}
