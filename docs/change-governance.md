# Change governance

The practice's own production systems (website, automation routes and data base) are run under the same discipline it assesses.

- **Audit before change.** Every change is reviewed against the live system, never from memory or documentation alone.
- **Approval by the accountable owner.** Each change is approved in a decision record before it is made, then read back after it is made.
- **Separation of duties.** The builder writes changes to staging only. Publishing to production is done by the owner.
- **Open items register.** Every open issue gets a permanent reference that is never reused. Closing an item means striking it with what closed it and when. The register is versioned at every working session.

## Metrics

Over register versions 9 to 15 (October 12 to 24, 2026), 43 items were closed. For the 14 items both opened and closed in that window, the median time from first listing to closure was three days. [tools/register_metrics.py](../tools/register_metrics.py) recomputes these figures and states its inclusion rules.
