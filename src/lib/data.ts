export type Comment = {
  id: string;
  author: string;
  authorAvatar: string;
  timestamp: string;
  text: string;
};

export type Ticket = {
  id: string;
  subject: string;
  description: string;
  status: "Open" | "In Progress" | "Resolved" | "Closed";
  category: string;
  author: string;
  authorEmail: string;
  createdAt: string;
  updatedAt: string;
  upvotes: number;
  downvotes: number;
  agent?: string;
  comments: Comment[];
};

export const categories = [
  "Billing",
  "Technical Support",
  "Account Access",
  "General Inquiry",
  "Feature Request",
];

export const tickets: Ticket[] = [
  {
    id: "TICK-001",
    subject: "Cannot login to the system",
    description:
      "I've been trying to log in for the past hour, but I keep getting an 'Invalid Credentials' error. I've tried resetting my password multiple times, but the issue persists. My username is 'john.doe'.",
    status: "Open",
    category: "Account Access",
    author: "John Doe",
    authorEmail: "john.d@example.com",
    createdAt: "2024-05-23T10:00:00Z",
    updatedAt: "2024-05-23T10:00:00Z",
    upvotes: 12,
    downvotes: 1,
    comments: [
      {
        id: "C1",
        author: "Jane Smith (Agent)",
        authorAvatar: "JS",
        timestamp: "2024-05-23T10:05:00Z",
        text: "Hi John, I'm looking into this for you. Can you confirm if you are using the correct email address associated with your account?",
      },
    ],
  },
  {
    id: "TICK-002",
    subject: "API endpoint returning 500 error",
    description: "The `/api/v2/users` endpoint is consistently returning a 500 Internal Server Error. This started about 30 minutes ago. No changes were made on our end. This is a critical issue for our integration.",
    status: "In Progress",
    category: "Technical Support",
    author: "Jane Doe",
    authorEmail: "jane.d@example.com",
    createdAt: "2024-05-23T09:30:00Z",
    updatedAt: "2024-05-23T11:45:00Z",
    upvotes: 25,
    downvotes: 0,
    agent: "Bob Johnson",
    comments: [
        {
            id: "C1",
            author: "Bob Johnson (Agent)",
            authorAvatar: "BJ",
            timestamp: "2024-05-23T09:35:00Z",
            text: "Hi Jane, thanks for reporting. We've identified an issue with a recent deployment and our engineering team is actively working on a fix. I'll post an update here as soon as I have one.",
        },
        {
            id: "C2",
            author: "Bob Johnson (Agent)",
            authorAvatar: "BJ",
            timestamp: "2024-05-23T11:45:00Z",
            text: "Update: A patch has been deployed and we're monitoring the situation. The API should be responding correctly now. Please let us know if you see any further issues.",
        }
    ]
  },
  {
    id: "TICK-003",
    subject: "Question about latest invoice",
    description: "I received my invoice for May and there's a charge I don't recognize. It's listed as 'Service Adjustment Fee'. Can you please provide more details on what this is for?",
    status: "Resolved",
    category: "Billing",
    author: "Peter Jones",
    authorEmail: "peter.j@example.com",
    createdAt: "2024-05-22T14:00:00Z",
    updatedAt: "2024-05-22T16:20:00Z",
    upvotes: 2,
    downvotes: 0,
    agent: "Alice Williams",
    comments: [
        {
            id: "C1",
            author: "Alice Williams (Agent)",
            authorAvatar: "AW",
            timestamp: "2024-05-22T14:15:00Z",
            text: "Hi Peter, I can certainly clarify that for you. That fee is related to the additional user licenses you added mid-cycle last month. I've attached a detailed breakdown to this ticket. I'll mark this as resolved, but feel free to reopen if you have more questions!",
        }
    ]
  },
  {
    id: "TICK-004",
    subject: "How do I export my data?",
    description: "I need to export all of my project data into a CSV format for an internal audit. I can't seem to find the export feature in the dashboard. Is this possible?",
    status: "Closed",
    category: "General Inquiry",
    author: "Mary Davis",
    authorEmail: "mary.d@example.com",
    createdAt: "2024-05-21T11:10:00Z",
    updatedAt: "2024-05-21T11:30:00Z",
    upvotes: 8,
    downvotes: 1,
    agent: "Jane Smith",
    comments: [
        {
            id: "C1",
            author: "Jane Smith (Agent)",
            authorAvatar: "JS",
            timestamp: "2024-05-21T11:25:00Z",
            text: "Hello Mary, you can find the data export functionality under 'Settings' > 'Data Management'. From there, you can select the date range and format for your export. Let me know if you need any more help!",
        }
    ]
  },
   {
    id: "TICK-005",
    subject: "Request for Dark Mode feature",
    description: "Our team primarily works in low-light environments, and the current bright UI can be strenuous on the eyes. We would love to see a dark mode option added to the application. This would be a huge improvement for us.",
    status: "Open",
    category: "Feature Request",
    author: "Chris Green",
    authorEmail: "chris.g@example.com",
    createdAt: "2024-05-23T15:00:00Z",
    updatedAt: "2024-05-23T15:05:00Z",
    upvotes: 42,
    downvotes: 0,
    comments: [
      {
        id: "C1",
        author: "Alice Williams (Agent)",
        authorAvatar: "AW",
        timestamp: "2024-05-23T15:05:00Z",
        text: "Hi Chris, thank you for the suggestion! This is a popular request, and I've added your vote to the internal tracking ticket. We'll be sure to announce it if it gets added to our roadmap.",
      },
    ],
  },
];
