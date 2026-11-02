# Building with AI agents under change governance

I use Claude, ChatGPT and Microsoft Copilot in daily work. For the practice's production systems, I direct an AI agent (Claude) that is connected to Airtable, Make, Webflow and Microsoft 365 through Model Context Protocol (MCP) connectors.

## How the work is governed

| Control | How it works |
|---|---|
| Accountable owner | I approve every change before it is released. The agent proposes and builds; it does not decide. |
| Read before write | The agent reads the live configuration before specifying any change to it, and reads it back afterwards. |
| Drafts first | Automation edits stay drafts until I publish them; website changes are published only by me. |
| Secrets stay out of chat | Keys go straight into the platform that uses them. Integrations that hold a secret are edited by me, not the agent. |
| Money stays with a person | The agent never sends invoices, takes payments or issues refunds. |
| Evidence | Each build ends with a written validation record of what was tested and what was observed, and the open-items register is updated at every close. |

## What this produced

The launch described in [integration-platform.md](integration-platform.md), built this way between October and November 2026, with the tests recorded in [validation/launch-and-payments-validation.md](validation/launch-and-payments-validation.md).
