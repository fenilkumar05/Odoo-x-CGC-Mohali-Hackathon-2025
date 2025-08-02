"use server";

import { suggestTicketCategory } from "@/ai/flows/suggest-ticket-category";
import { z } from "zod";

const schema = z.object({
  subject: z.string().min(1, { message: "Subject is required." }),
  description: z.string().min(1, { message: "Description is required." }),
});

export async function getCategorySuggestion(data: {
  subject: string;
  description: string;
}) {
  const parsedData = schema.safeParse(data);
  if (!parsedData.success) {
    return { category: null, error: "Subject and description are required." };
  }

  try {
    const result = await suggestTicketCategory(parsedData.data);
    return { category: result.category, error: null };
  } catch (e) {
    console.error(e);
    return { category: null, error: "Failed to get AI suggestion." };
  }
}
