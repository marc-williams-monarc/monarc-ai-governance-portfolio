# Architecture

How a request, an assessment and a score move through the practice's systems. Booking, invitations and payments are shown in [integration-platform.md](integration-platform.md). The web forms run on Webflow, the routes on Make, and the records live in Airtable; email and alerts go through Microsoft 365 and Teams.

```mermaid
flowchart LR
  A[Website form] -->|bot check token| B[Make route]
  B -->|verify token with Cloudflare| C{Verified and complete?}
  C -- no --> R[Reject: nothing stored]
  C -- yes --> D[(Airtable: request record)]
  D --> E[Alert to the accountable person]
  D --> F[Assessment record]
  F --> G[AI drafts from metadata only]
  G --> H{Human review gate}
  H -- approved --> I[Score issued: Active]
  I --> J[Daily lapse check]
  I --> K[Re-assessment reminders: 90, 180, 365 days]
  I --> L[Status-change log]
  M[Relying party: status request] --> B2[Make route] --> N[(Status requests)] --> O[Human confirms the firm's consent]
```

## Design rules

- **AI drafts, a person decides.** No score or finding reaches anyone without a named person's review.
- **Least privilege.** Connections to Microsoft 365 use scoped Microsoft Graph permissions with administrator consent.
- **Nothing trusted from the browser.** Every form is checked server-side for a valid bot-check token and complete fields before anything is stored. Rejected requests leave no record.
- **Every status change is logged.** The log records who changed what and why, and its rows are never edited.
- **Secrets stay in the platforms.** Keys live in Make and Cloudflare, never in page code or documents.
