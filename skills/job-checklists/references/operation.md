# Operating a checklist

1. Read ready setup and approved template version. If answers changed, update setup and confirm only affected decisions. Existing instances retain their original requirements unless an authorized change is recorded.
2. Obtain a stable job/occurrence key from the chosen source. Replayed triggers use the same key; a new day/shift uses a distinct key when configured that way. Check for an existing instance before generation or delivery.
3. Bind actual job details to task IDs. Missing required details create a blocked draft; never invent addresses, materials, staffing, due times or operating requirements.
4. Apply the generation/dispatch policies separately. A generated draft is not assigned. Record delivery ID, recipient and outcome in the selected system. If sending times out, reconcile with delivery history before retrying; unknown is not failed.
5. Let the assignee complete or flag individual tasks. Capture evidence only as configured. Preserve job ID, task ID, actor, timestamp and changes where history is required. Corrections/reopens add events rather than erase previous completion.
6. Summarize outstanding/blocked work from the actual current state, including freshness/source. Do not interpret all boxes checked as independently verified work. Close only under the agreed review rule.
7. Handle schedule changes and cancellation by updating/suspending pending notifications. Stop reminders after completion/cancellation. Apply quiet hours and limits in the runtime, not just in prose.

## Local helper

Use a template JSON with `version` and `tasks`, each task containing unique `id` and `text`. The helper never executes task text. Example synthetic template:

```json
{"version":"1","tasks":[{"id":"arrival","text":"Confirm the approved job scope"},{"id":"closeout","text":"Record any blocked work"}]}
```

Run `python3 <skill>/scripts/checklist.py --help`. Commands `create`, `update`, `show` need an explicit `--data-dir` outside the skill/repository. `create` snapshots a template under a job ID; repeated same-key/same-input calls are idempotent, conflicting calls fail. `update` records state events; `show` renders Markdown to stdout. No delivery, authentication, reminder service, hosted endpoint or sync is provided.

The event file is locally editable and actors are self-reported. Use a shared system for multiple writers, remote checkoff or reliable attribution. Back up private records using the user's selected mechanism, never by committing them to this public repository.
