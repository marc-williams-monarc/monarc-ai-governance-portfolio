# AI governance portfolio · Marc Williams

Working evidence for the architecture, integration and AI governance work described on my résumé. It is published by Monarc Technology Group LLC, the practice I founded and lead.

**Status, stated plainly:** Monarc was established in 2019 and launched its first website in 2023. The redesigned website launched on October 27, 2026, and live payments and automated invoicing went live on November 1, 2026. Every test described here used synthetic records or my own transactions (including a real $1 payment and refund), so no client data appears in this repository. Client systems, credentials, webhook addresses, record IDs, scoring weights and proprietary method detail are deliberately left out.

## Where each claim is shown

| Résumé claim | Evidence here |
|---|---|
| Launched the production platform: website, booking and calendar-invitation workflows, live Stripe payments and automated invoicing, integrated through REST APIs and webhooks and run by 22 Airtable automations | [docs/integration-platform.md](docs/integration-platform.md) · [docs/validation/launch-and-payments-validation.md](docs/validation/launch-and-payments-validation.md) |
| Hands-on with AI platforms; AI agents connected to production systems through Model Context Protocol (MCP), under change governance | [docs/ai-agent-delivery.md](docs/ai-agent-delivery.md) |
| Designed, built and tested the governance lifecycle: intake, assessment, classification, human review gate, approval, ongoing oversight | [docs/architecture.md](docs/architecture.md) · [docs/governance-lifecycle.md](docs/governance-lifecycle.md) · [docs/validation/score-status-validation.md](docs/validation/score-status-validation.md) |
| Agentic AI governance standards: execution authority, stop controls, named human accountability, conditions for expanding authority | [docs/agentic-ai-standard.md](docs/agentic-ai-standard.md) |
| Tested control design and operating effectiveness; found a defect hidden by offsetting errors | [docs/validation/assessment-scoring-validation.md](docs/validation/assessment-scoring-validation.md) |
| Change governance, with open items tracked to closure | [docs/change-governance.md](docs/change-governance.md) |
| 43 open items closed in 12 days, median three days to closure | [tools/register_metrics.py](tools/register_metrics.py) recomputes the figures from [tools/data/register_closures.csv](tools/data/register_closures.csv) |
| 25 of 25 end-to-end intake test runs successful since the last credential fix (October 18 to 31) | [docs/validation/launch-and-payments-validation.md](docs/validation/launch-and-payments-validation.md#intake-reliability) |
| Automated change traceability across operational data | [patterns/audit-log](patterns/audit-log) |
| Mapped the assessment to EU AI Act deployer and human oversight obligations | [docs/eu-ai-act-mapping.md](docs/eu-ai-act-mapping.md) |
| Evidentiary record architecture (hashes, append-only log, independent timestamping) | [evidence-record/](evidence-record): working code with tests |

## Running the code

```bash
cd evidence-record && python -m pytest -q        # 10 tests
python tools/register_metrics.py                  # recomputes the register metrics
```

Python 3.9 or later. No third-party packages are needed except pytest to run the tests.

## Contact

Marc Williams · [linkedin.com/in/marc-williams-monarc](https://www.linkedin.com/in/marc-williams-monarc) · [monarcgroupllc.com](https://www.monarcgroupllc.com)

© 2026 Monarc Technology Group LLC. All rights reserved unless a file says otherwise.
