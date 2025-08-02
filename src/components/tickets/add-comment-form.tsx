"use client";

import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useToast } from "@/hooks/use-toast";
import { Send } from "lucide-react";
import React from "react";

export function AddCommentForm() {
  const { toast } = useToast();
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const form = e.target as HTMLFormElement;
    const textarea = form.elements.namedItem("comment") as HTMLTextAreaElement;
    if (textarea.value.trim()) {
      toast({
        title: "Comment Added",
        description: "Your comment has been posted.",
      });
      textarea.value = "";
    }
  };

  return (
    <form className="mt-6 flex flex-col gap-4" onSubmit={handleSubmit}>
        <Textarea
          name="comment"
          placeholder="Add your reply..."
          className="min-h-[120px]"
        />
        <Button type="submit" className="self-end">
            <Send className="mr-2 h-4 w-4" />
            Add Reply
        </Button>
    </form>
  );
}
