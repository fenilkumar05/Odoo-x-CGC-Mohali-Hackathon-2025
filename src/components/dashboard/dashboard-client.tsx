"use client";

import * as React from "react";
import { Ticket, categories } from "@/lib/data";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { TicketTable } from "./ticket-table";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Button } from "../ui/button";
import { ListFilter, PlusCircle } from "lucide-react";
import {
    DropdownMenu,
    DropdownMenuCheckboxItem,
    DropdownMenuContent,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
  } from "@/components/ui/dropdown-menu"
import Link from "next/link";

type DashboardClientProps = {
  initialTickets: Ticket[];
};

export function DashboardClient({ initialTickets }: DashboardClientProps) {
  const [tickets, setTickets] = React.useState(initialTickets);
  const [filters, setFilters] = React.useState({
    status: "all",
    category: "all",
    ownTickets: false,
  });
  const [sort, setSort] = React.useState("recently-modified");

  React.useEffect(() => {
    let filtered = [...initialTickets];

    if (filters.status !== "all") {
      filtered = filtered.filter(
        (t) => t.status.toLowerCase().replace(" ", "-") === filters.status
      );
    }

    if (filters.category !== "all") {
      filtered = filtered.filter((t) => t.category === filters.category);
    }
    
    // Note: 'ownTickets' filter would need user context, mocked for now
    if (filters.ownTickets) {
       filtered = filtered.filter(t => t.authorEmail === 'admin@desknow.com' || t.author === 'John Doe');
    }

    if(sort === 'recently-modified') {
        filtered.sort((a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime());
    } else if (sort === 'most-replied') {
        filtered.sort((a,b) => b.comments.length - a.comments.length)
    }

    setTickets(filtered);
  }, [filters, sort, initialTickets]);
  
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>All Tickets</CardTitle>
        <div className="flex items-center gap-2">
           <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline" size="sm" className="h-8 gap-1">
                  <ListFilter className="h-3.5 w-3.5" />
                  <span className="sr-only sm:not-sr-only sm:whitespace-nowrap">
                    Filter
                  </span>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuLabel>Filter by</DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuCheckboxItem checked={filters.status === 'open'} onCheckedChange={(checked) => setFilters({...filters, status: checked ? 'open' : 'all'})}>
                  Open
                </DropdownMenuCheckboxItem>
                 <DropdownMenuCheckboxItem checked={filters.status === 'in-progress'} onCheckedChange={(checked) => setFilters({...filters, status: checked ? 'in-progress' : 'all'})}>
                  In Progress
                </DropdownMenuCheckboxItem>
                 <DropdownMenuCheckboxItem checked={filters.ownTickets} onCheckedChange={(checked) => setFilters({...filters, ownTickets: !!checked })}>
                  My Tickets
                </DropdownMenuCheckboxItem>
              </DropdownMenuContent>
            </DropdownMenu>
            <Link href="/tickets/new">
                <Button size="sm" className="h-8 gap-1">
                <PlusCircle className="h-3.5 w-3.5" />
                <span className="sr-only sm:not-sr-only sm:whitespace-nowrap">
                    Create Ticket
                </span>
                </Button>
            </Link>
        </div>
      </CardHeader>
      <CardContent>
         <div className="mb-4 flex items-center gap-4">
          <Select
            value={filters.category}
            onValueChange={(value) => setFilters({ ...filters, category: value })}
          >
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="All Categories" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Categories</SelectItem>
              {categories.map((cat) => (
                <SelectItem key={cat} value={cat}>
                  {cat}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Select value={sort} onValueChange={setSort}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Sort by" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="recently-modified">Recently Modified</SelectItem>
              <SelectItem value="most-replied">Most Replied</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <TicketTable tickets={tickets} />
      </CardContent>
    </Card>
  );
}
