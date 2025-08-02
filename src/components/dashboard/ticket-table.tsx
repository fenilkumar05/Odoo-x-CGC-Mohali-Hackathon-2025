"use client";

import * as React from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Eye, ThumbsDown, ThumbsUp } from "lucide-react";
import { Ticket } from "@/lib/data";
import { useRouter } from "next/navigation";
import { format, parseISO } from "date-fns";

type TicketTableProps = {
  tickets: Ticket[];
};

export function TicketTable({ tickets }: TicketTableProps) {
  const router = useRouter();
  const [currentPage, setCurrentPage] = React.useState(1);
  const ticketsPerPage = 5;

  const statusVariantMap: {
    [key in Ticket["status"]]: "default" | "secondary" | "destructive" | "outline";
  } = {
    Open: "destructive",
    "In Progress": "default",
    Resolved: "secondary",
    Closed: "outline",
  };
  
  const indexOfLastTicket = currentPage * ticketsPerPage;
  const indexOfFirstTicket = indexOfLastTicket - ticketsPerPage;
  const currentTickets = tickets.slice(indexOfFirstTicket, indexOfLastTicket);

  const paginate = (pageNumber: number) => setCurrentPage(pageNumber);

  return (
    <div>
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Subject</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Category</TableHead>
              <TableHead>Last Updated</TableHead>
              <TableHead>Votes</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {currentTickets.map((ticket) => (
              <TableRow key={ticket.id}>
                <TableCell className="font-medium">
                  <div className="flex flex-col">
                    <span className="font-semibold">{ticket.subject}</span>
                    <span className="text-xs text-muted-foreground">{ticket.id} by {ticket.author}</span>
                  </div>
                </TableCell>
                <TableCell>
                  <Badge variant={statusVariantMap[ticket.status]}>
                    {ticket.status}
                  </Badge>
                </TableCell>
                <TableCell>{ticket.category}</TableCell>
                <TableCell>
                  {format(parseISO(ticket.updatedAt), "MMM d, yyyy")}
                </TableCell>
                <TableCell>
                    <div className="flex items-center gap-2">
                        <div className="flex items-center gap-1 text-green-600">
                            <ThumbsUp className="h-4 w-4"/>
                            <span className="text-xs">{ticket.upvotes}</span>
                        </div>
                         <div className="flex items-center gap-1 text-red-600">
                            <ThumbsDown className="h-4 w-4"/>
                            <span className="text-xs">{ticket.downvotes}</span>
                        </div>
                    </div>
                </TableCell>
                <TableCell className="text-right">
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => router.push(`/tickets/${ticket.id}`)}
                  >
                    <Eye className="h-4 w-4" />
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
      <div className="flex justify-end space-x-2 py-4">
        <Button
          variant="outline"
          size="sm"
          onClick={() => paginate(currentPage - 1)}
          disabled={currentPage === 1}
        >
          Previous
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => paginate(currentPage + 1)}
          disabled={indexOfLastTicket >= tickets.length}
        >
          Next
        </Button>
      </div>
    </div>
  );
}
