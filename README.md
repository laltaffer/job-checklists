# Job Checklists for Codex

A reusable skill that helps an owner turn operating procedures into job checklists, choose how much control to keep, and test assignment and completion with an assignee.

Start with guided setup. It asks whether tasks repeat, whether each job/day needs a fresh list, what completion history matters, where people will check things off, and which actions should run automatically. Setup can be saved and resumed. No other skill, API key or subscription is required to read/use the workflow. The optional local helper requires Python 3.9+.

## Install

Clone this public repository, inspect it, then copy the skill with the installer:

```sh
git clone https://github.com/laltaffer/job-checklists.git
cd job-checklists
python3 install.py
```

The installer copies only `skills/job-checklists` into `~/.agents/skills/job-checklists`, refuses to replace an existing installation, and does not modify Codex settings or start automation. For a different Codex skill directory, pass `--destination /absolute/path/to/skills`. Restart Codex or open a new session if necessary for skill discovery.

Then ask Codex:

> Use $job-checklists to set up checklists for my team. Help me decide how they should be created, assigned and checked off.

For an update, inspect the new version and move/remove the old installed copy yourself before reinstalling; the installer does not erase it.

## What is included

- Branching setup interview with saved decisions and a test rehearsal.
- Instructions for reusable templates, fresh job instances, reminders and action-level permissions.
- A Python local checklist helper with duplicate protection and completion event history.
- A guide for choosing an existing shared tool or specifying a hosted system when needed.

**This is a Codex skill, not a hosted checklist app.** Installation does not give workers a phone interface, connect a CRM, send messages or run background jobs. Those capabilities depend on the route chosen during setup and must be implemented and tested separately. Local completion labels are self-reported and the local event ledger is not tamper-proof.

Keep real SOPs, setup answers and job data in a private workspace outside this checkout. All public examples are synthetic.

## Validate

```sh
python3 -m unittest discover -s tests -v
```

See [SKILL.md](skills/job-checklists/SKILL.md) for the workflow. MIT licensed.
