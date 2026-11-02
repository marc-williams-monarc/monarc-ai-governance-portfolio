# Audit-log pattern

Every operational table has a small automation. When a record is created, or a watched field such as a score's status changes, it writes a row to an append-only log recording:
- the table and record;
- the action and the field that changed;
- the old and new values;
- who held authority for the change;
- a server-set timestamp.

Log rows are never edited. Corrections are new rows.

`log_change.js` is a simplified example of the pattern for an Airtable automation script, not the live code. The live scripts send to an authenticated endpoint whose address and key are kept in the platform, never in code.
