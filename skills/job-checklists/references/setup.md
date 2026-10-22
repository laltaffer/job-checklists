# Guided setup

Goal: understand what the owner wants to delegate, not sell them software. Use one real example. Present 2–3 answerable questions per round, with a plain-language recommendation. Let the owner answer conversationally. Inspect authorized existing documents/settings yourself for factual answers; don't ask them to know integration jargon.

## Decision tree

### Round 1 — outcome and people

- What do you currently have to chase or remember, and what would you like to stop doing?
- Who prepares work, who carries it out, and who reviews it? Who covers absences?
- Walk through one recent job: how did the assignee learn the tasks, report completion, and flag a problem?

Record known SOPs and the existing job system. Do not infer employee status or invent tasks. If no written SOP exists, capture the owner's dictated process and have them correct it.

### Round 2 — list shape (depends on the example)

Ask which fits: same standard tasks; a fresh custom list each job; standard tasks plus job-specific additions. Recommend a versioned base plus reviewed job-specific details if they have repeatable work with exceptions.

Then ask granularity: one checklist per job, per worker, per day/shift, or another occurrence? Can a multi-day job have daily required tasks? Can tasks be not applicable, blocked or reopened? What evidence is required on which tasks (none, note, photo, quantity)? Avoid making every task require a photo.

Separate reusable content from completed instances. If the owner wants one resetting list, ask whether past completion should be retained before choosing reset semantics.

### Round 3 — records and access (depends on chosen list shape)

Do they need only current progress, or who checked what and when for each job? How long must records/evidence be retained? Who can see or change them? Is individual attribution important or is a shared team acknowledgement enough?

Where will assignees open it: phone app, browser link, existing job system, paper? Must they work offline? Should the owner see a live status view, a completion notice or an exception digest? If accounts are burdensome, explain the tradeoff of a shared link: anyone holding it may act, and identity attribution is weaker.

If records or remote participation are needed, branch to shared-system.md. Do not equate history with mandatory custom hosting; an existing tool may already provide it.

### Round 4 — automation and control (depends on source and destination)

Ask for each action whether it should be manual, prepared for approval, or automatic within agreed rules:

1. Generate a checklist.
2. Assign/send it to the recipient.
3. Send reminders.
4. Escalate overdue or blocked work.
5. Change a checklist after assignment.
6. Close/reopen a job.

Then establish the trigger (accepted quote, scheduled job, daily time or explicit command), where that fact lives, who receives what, how changes/cancellations work, and when reminders become annoying. Ask timezone, quiet hours, maximum reminder frequency, escalation recipient, and how automation stops. Identify what happens when the source is missing or a delivery attempt has an unknown outcome.

If the answer is “fully automatic,” translate it into this concrete action policy and read it back. Don't quietly narrow full automation to draft-only, or treat it as permission for every future action.

### Round 5 — choose the smallest usable route

Offer one recommendation and explain its limits:

- Local/paper: simplest if no shared state or verified attribution is needed.
- Existing shared tool: first choice when it already supports required access/history.
- Hosted workflow: when the required shared experience cannot be met otherwise; requires separate provider/access/cost decisions and implementation.

Confirm monthly budget, who pays/owns the account, who maintains it and what happens when they leave. Mark unavailable capabilities unverified until checked in the actual account. Do not start a product comparison unless it changes the decision.

## Save and resume

Save this JSON structure with real confirmed values, leaving unanswered fields null. Enumerated action modes: `manual`, `approval`, `automatic`. Not applicable fields may use `not_applicable` with a reason in notes. Do not put passwords or secret links in it.

```json
{
  "schema_version": 1,
  "status": "draft",
  "outcome": null,
  "roles": {"owner": null, "assignee": null, "reviewer": null, "backup": null},
  "template": {"mode": null, "source": null, "version": null, "approved_by": null},
  "occurrence": {"unit": null, "key_rule": null, "timezone": null},
  "tasks": {"granularity": null, "allowed_states": null, "evidence_rules": null},
  "records": {"history": null, "attribution": null, "retention": null, "access": null},
  "delivery": {"system": null, "channel": null, "recipient_rule": null, "offline": null},
  "control": {"generate": null, "dispatch": null, "remind": null, "escalate": null, "edit": null, "close": null},
  "automation": {"state": "planned", "trigger_source": null, "trigger_rule": null, "quiet_hours": null, "reminder_limit": null, "failure_owner": null, "pause_method": null, "runtime_id": null},
  "test": {"job": null, "result": null, "review_date": null},
  "owner_confirmation": null
}
```

The notes file records decisions, reasons, unresolved questions, existing-system checks and the next interview question. A ready setup requires resolved decisions for the chosen route, an approved template, the owner's explicit confirmation and a test plan. Runtime ID can remain null while planned; ready setup does not mean live automation. Manual operation may be ready with automation fields explicitly not applicable.

## Acceptance rehearsal

Have the owner prepare one instance, an assignee/test user open it on their intended device, complete a task, report a blocker, and let the owner see both. Then create a second occurrence and confirm its boxes start unchecked without changing the first record. Try a duplicate trigger and a changed/cancelled job. Label simulated identities and deliveries. Record actual results; no real deployment or verified identity can be inferred from a local demo.
