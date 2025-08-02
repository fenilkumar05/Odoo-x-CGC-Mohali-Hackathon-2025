import { tickets } from "@/lib/data";
import { TicketDetailClient } from "@/components/tickets/ticket-detail-client";
import { notFound } from "next/navigation";

type TicketDetailPageProps = {
  params: {
    id: string;
  };
};

export default function TicketDetailPage({ params }: TicketDetailPageProps) {
  // In a real app, you would fetch this data from an API
  const ticket = tickets.find((t) => t.id === params.id);

  if (!ticket) {
    notFound();
  }

  return (
    <div>
      <TicketDetailClient ticket={ticket} />
    </div>
  );
}
