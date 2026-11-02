// Airtable automation script (example pattern, not live code).
// Trigger: "When a record is created" or "When a record is updated" (watching one field).
// Input variables configured in the automation: tableName, recordId, fieldName, newValue, reason.
// The logging endpoint and its key are stored as automation secrets, never in the script.

const cfg = input.config();
const endpoint = input.secret('AUDIT_ENDPOINT');   // set in the automation, not here
const apiKey = input.secret('AUDIT_API_KEY');

const row = {
  action: cfg.fieldName ? 'STATUS_CHANGE' : 'CREATE',
  table_name: cfg.tableName,
  record_id: cfg.recordId,
  field_changed: cfg.fieldName || 'record_created',
  new_value: cfg.newValue ? String(cfg.newValue) + (cfg.reason ? ' · ' + cfg.reason : '') : '',
  // The receiving system adds the timestamp so the record's author cannot set it.
};

const res = await fetch(endpoint, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-make-apikey': apiKey },
  body: JSON.stringify(row),
});
if (!res.ok) throw new Error('Audit log write failed: HTTP ' + res.status); // fail loudly, never silently
output.set('logged', true);
