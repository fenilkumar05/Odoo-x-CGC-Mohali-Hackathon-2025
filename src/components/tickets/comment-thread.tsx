import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Card, CardContent } from "@/components/ui/card";
import { Comment } from "@/lib/data";
import { formatDistanceToNow, parseISO } from "date-fns";

type CommentThreadProps = {
  comments: Comment[];
};

export function CommentThread({ comments }: CommentThreadProps) {
  return (
    <div className="space-y-6">
      {comments.map((comment, index) => (
        <div key={comment.id} className="flex gap-4">
          <Avatar className="h-10 w-10">
            <AvatarImage
              src={`https://i.pravatar.cc/150?u=${comment.author
                .split(" ")[0]
                .toLowerCase()}`}
            />
            <AvatarFallback>{comment.authorAvatar}</AvatarFallback>
          </Avatar>
          <div className="flex-1">
            <Card>
              <CardContent className="p-4">
                <div className="mb-2 flex items-center justify-between">
                  <p className="font-semibold">{comment.author}</p>
                  <p className="text-xs text-muted-foreground">
                    {formatDistanceToNow(parseISO(comment.timestamp), {
                      addSuffix: true,
                    })}
                  </p>
                </div>
                <p className="text-sm text-foreground/90">{comment.text}</p>
              </CardContent>
            </Card>
          </div>
        </div>
      ))}
    </div>
  );
}
