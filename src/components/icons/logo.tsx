import { Ticket } from "lucide-react";
import { cn } from "@/lib/utils";

export function Logo({ className }: { className?: string }) {
  return (
    <div
      className={cn(
        "flex items-center gap-2 text-lg font-bold text-foreground",
        className
      )}
    >
      <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
        <Ticket className="h-5 w-5 text-primary-foreground" />
      </div>
      <span className="font-headline">DeskNow</span>
    </div>
  );
}
