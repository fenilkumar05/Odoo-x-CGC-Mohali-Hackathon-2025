"use client";

import { Ticket } from "@/lib/data";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  CardFooter
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ThumbsDown, ThumbsUp, User, Calendar, Tag } from "lucide-react";
import { Separator } from "@/components/ui/separator";
import { CommentThread } from "./comment-thread";
import { AddCommentForm } from "./add-comment-form";
import { format, parseISO } from "date-fns";
import React from "react";

type TicketDetailClientProps = {
  ticket: Ticket;
};

export function TicketDetailClient({ ticket }: TicketDetailClientProps) {
    const [votes, setVotes] = React.useState({upvotes: ticket.upvotes, downvotes: ticket.downvotes});

    const handleVote = (type: 'up' | 'down') => {
        if(type === 'up') {
            setVotes(v => ({...v, upvotes: v.upvotes + 1}));
        } else {
            setVotes(v => ({...v, downvotes: v.downvotes + 1}));
        }
    }

  const statusVariantMap: {
    [key in Ticket["status"]]: "default" | "secondary" | "destructive" | "outline";
  } = {
    Open: "destructive",
    "In Progress": "default",
    Resolved: "secondary",
    Closed: "outline",
  };

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
      <div className="space-y-6 lg:col-span-2">
        <Card>
          <CardHeader>
            <div className="flex items-start justify-between">
              <div>
                <Badge variant={statusVariantMap[ticket.status]}>
                  {ticket.status}
                </Badge>
                <CardTitle className="mt-2 text-2xl">{ticket.subject}</CardTitle>
                <CardDescription>Ticket ID: {ticket.id}</CardDescription>
              </div>
              <div className="flex items-center gap-2">
                <Button variant="outline" size="sm" onClick={() => handleVote('up')}>
                  <ThumbsUp className="mr-2 h-4 w-4 text-green-500" /> {votes.upvotes}
                </Button>
                <Button variant="outline" size="sm" onClick={() => handleVote('down')}>
                  <ThumbsDown className="mr-2 h-4 w-4 text-red-500" /> {votes.downvotes}
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <p className="text-foreground/90">{ticket.description}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Conversation</CardTitle>
          </CardHeader>
          <CardContent>
            <CommentThread comments={ticket.comments} />
            <Separator className="my-6" />
            <AddCommentForm />
          </CardContent>
        </Card>
      </div>

      <div className="space-y-6 lg:col-span-1">
        <Card>
          <CardHeader>
            <CardTitle>Ticket Details</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4 text-sm">
            <div className="flex items-center">
              <User className="mr-3 h-5 w-5 text-muted-foreground" />
              <div>
                <p className="font-semibold">Submitted by</p>
                <p>{ticket.author}</p>
              </div>
            </div>
            <div className="flex items-center">
              <Calendar className="mr-3 h-5 w-5 text-muted-foreground" />
              <div>
                <p className="font-semibold">Created On</p>
                <p>{format(parseISO(ticket.createdAt), "PPP")}</p>
              </div>
            </div>
            <div className="flex items-center">
              <Calendar className="mr-3 h-5 w-5 text-muted-foreground" />
              <div>
                <p className="font-semibold">Last Updated</p>
                <p>{format(parseISO(ticket.updatedAt), "PPP")}</p>
              </div>
            </div>
            <div className="flex items-center">
              <Tag className="mr-3 h-5 w-5 text-muted-foreground" />
              <div>
                <p className="font-semibold">Category</p>
                <p>{ticket.category}</p>
              </div>
            </div>
             <div className="flex items-center">
              <User className="mr-3 h-5 w-5 text-muted-foreground" />
              <div>
                <p className="font-semibold">Assigned Agent</p>
                <p>{ticket.agent || 'Unassigned'}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
