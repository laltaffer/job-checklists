# Shared completion and retained records

First inspect the authorized existing job tool for mobile checklists, reusable templates, assignments, attachments, history and triggers. Don't promise a vendor feature from memory. Run a real two-role rehearsal before recommending migration or calling it live.

If the owner only has email and spreadsheets, identify the provider first. Check whether an existing shared workbook or form can give each worker a fresh job/day record on their phone, preserve prior submissions, show blockers and restrict access as required. Test two users and two occurrences. Email may deliver a link; it does not supply shared completion state. A spreadsheet's edit history may not meet the owner's attribution requirement. If generation/reminders need a scheduler or connector, verify that separately. Prefer this route if it meets the chosen requirements; do not infer that a custom app is needed just because there is no dedicated job tool.

If a new hosted solution is needed, document a small implementation brief, not an imaginary deployed service:

- Job, template version, task instance, assignment, event and evidence records.
- Owner versus assignee permissions; individual login versus shared-link tradeoffs.
- Unique occurrence keys; database-enforced duplicate prevention; immutable event history or explicitly weaker history semantics.
- Mobile checkoff, blocked/not-applicable states, reopening and accessible controls.
- Server timestamps and actor attribution appropriate to the chosen authentication.
- Private evidence storage and authorization on reads/writes; no public bucket or predictable job links as access control.
- Delivery source, actual supported integration and scheduler; retry/reconciliation, cancellations and notification caps.
- Timezone, connectivity/offline requirements and conflict behavior.
- Retention, export, deletion, backups, account ownership, running costs and pause/exit procedure.

A retained record proves the recorded action, not that the physical task occurred. Shared links cannot establish strong individual attribution. Don't deploy, buy hosting, create accounts or share job data until the owner has selected the route and authorized those actions. If a production application is needed, hand this brief and unresolved questions to their engineering workflow. Keep checklist drafting usable while implementation is pending.
