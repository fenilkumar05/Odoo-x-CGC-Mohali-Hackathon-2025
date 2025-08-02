'use server';

/**
 * @fileOverview Suggests a category for a support ticket based on the subject and description.
 *
 * @fileOverview
 * - suggestTicketCategory - A function that suggests a ticket category.
 * - SuggestTicketCategoryInput - The input type for suggestTicketCategory.
 * - SuggestTicketCategoryOutput - The output type for suggestTicketCategory.
 */

import {ai} from '@/ai/genkit';
import {z} from 'genkit';

const SuggestTicketCategoryInputSchema = z.object({
  subject: z.string().describe('The subject of the support ticket.'),
  description: z.string().describe('The description of the support ticket.'),
});
export type SuggestTicketCategoryInput = z.infer<
  typeof SuggestTicketCategoryInputSchema
>;

const SuggestTicketCategoryOutputSchema = z.object({
  category: z.string().describe('The suggested category for the ticket.'),
});
export type SuggestTicketCategoryOutput = z.infer<
  typeof SuggestTicketCategoryOutputSchema
>;

export async function suggestTicketCategory(
  input: SuggestTicketCategoryInput
): Promise<SuggestTicketCategoryOutput> {
  return suggestTicketCategoryFlow(input);
}

const prompt = ai.definePrompt({
  name: 'suggestTicketCategoryPrompt',
  input: {schema: SuggestTicketCategoryInputSchema},
  output: {schema: SuggestTicketCategoryOutputSchema},
  prompt: `Given the subject and description of a support ticket, suggest a category for the ticket.

Subject: {{{subject}}}
Description: {{{description}}}

Category:`,
});

const suggestTicketCategoryFlow = ai.defineFlow(
  {
    name: 'suggestTicketCategoryFlow',
    inputSchema: SuggestTicketCategoryInputSchema,
    outputSchema: SuggestTicketCategoryOutputSchema,
  },
  async input => {
    const {output} = await prompt(input);
    return output!;
  }
);
