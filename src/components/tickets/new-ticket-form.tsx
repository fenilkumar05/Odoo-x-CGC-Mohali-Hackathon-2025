"use client";

import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { categories } from "@/lib/data";
import { Wand2, Loader2 } from "lucide-react";
import { useState } from "react";
import { getCategorySuggestion } from "@/app/(main)/tickets/new/actions";
import { useToast } from "@/hooks/use-toast";
import { useRouter } from "next/navigation";

const formSchema = z.object({
  subject: z.string().min(5, "Subject must be at least 5 characters."),
  category: z.string({ required_error: "Please select a category." }),
  description: z
    .string()
    .min(20, "Description must be at least 20 characters."),
  attachment: z.any().optional(),
});

export function NewTicketForm() {
  const [isSuggesting, setIsSuggesting] = useState(false);
  const { toast } = useToast();
  const router = useRouter();

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      subject: "",
      description: "",
    },
  });

  const handleSuggestCategory = async () => {
    const subject = form.getValues("subject");
    const description = form.getValues("description");

    if (!subject || !description) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Please enter a subject and description first.",
      });
      return;
    }

    setIsSuggesting(true);
    const result = await getCategorySuggestion({ subject, description });
    setIsSuggesting(false);

    if (result.error) {
      toast({
        variant: "destructive",
        title: "Suggestion Failed",
        description: result.error,
      });
    } else if (result.category) {
      form.setValue("category", result.category, { shouldValidate: true });
      toast({
        title: "Category Suggested!",
        description: `We've selected "${result.category}" for you.`,
      });
    }
  };

  function onSubmit(values: z.infer<typeof formSchema>) {
    console.log(values);
    toast({
        title: "Ticket Submitted!",
        description: "Your ticket has been created successfully.",
    });
    router.push('/dashboard');
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Create a New Support Ticket</CardTitle>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
            <FormField
              control={form.control}
              name="subject"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Subject</FormLabel>
                  <FormControl>
                    <Input placeholder="e.g., Unable to reset password" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="description"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Description</FormLabel>
                  <FormControl>
                    <Textarea
                      placeholder="Describe your issue in detail..."
                      className="min-h-[150px]"
                      {...field}
                    />
                  </FormControl>
                  <FormDescription>
                    The more details you provide, the faster we can help.
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />
            
            <div className="flex items-end gap-2">
                <FormField
                control={form.control}
                name="category"
                render={({ field }) => (
                    <FormItem className="flex-1">
                    <FormLabel>Category</FormLabel>
                    <Select onValueChange={field.onChange} value={field.value}>
                        <FormControl>
                        <SelectTrigger>
                            <SelectValue placeholder="Select a category" />
                        </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                        {categories.map((cat) => (
                            <SelectItem key={cat} value={cat}>
                            {cat}
                            </SelectItem>
                        ))}
                        </SelectContent>
                    </Select>
                    <FormMessage />
                    </FormItem>
                )}
                />
                <Button type="button" variant="outline" onClick={handleSuggestCategory} disabled={isSuggesting}>
                    {isSuggesting ? (
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    ) : (
                        <Wand2 className="mr-2 h-4 w-4" />
                    )}
                    Suggest
                </Button>
            </div>


            <FormField
              control={form.control}
              name="attachment"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Attachment (Optional)</FormLabel>
                  <FormControl>
                    <Input type="file" {...form.register("attachment")} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <Button type="submit">Submit Ticket</Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}
