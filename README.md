# Job Checklists for Codex

A reusable skill that helps an owner turn operating procedures into job checklists, choose how much control to keep, and test assignment and completion with an assignee.

Start with guided setup. It asks whether tasks repeat, whether each job/day needs a fresh list, what completion history matters, where people will check things off, and which actions should run automatically. Setup can be saved and resumed. No other skill, API key or subscription is required to read/use the workflow. The optional local helper requires Python 3.9+.

## Install by giving Codex this message

No terminal steps are required from the person installing it. Paste this into Codex:

> Install the Job Checklists skill from https://github.com/laltaffer/job-checklists/tree/main/skills/job-checklists, then walk me through setup for my team. Handle the installation for me; I do not use the terminal.

Codex can use its built-in skill installer with that direct GitHub skill-folder link. If installation requires a new turn or session for discovery, Codex should explain the one next step in plain language. It can read the installed instructions and begin setup in the current conversation when supported.

### Instructions for the installing Codex agent

1. Inspect the linked skill and use your available skill-installer capability to install `skills/job-checklists` from `laltaffer/job-checklists`. Do not install the whole repository as a skill or ask the person to execute shell commands.
2. Verify the installed `SKILL.md` and its supporting references/scripts exist. Respect an existing installation: inspect it and report whether it is current; do not delete or overwrite it silently.
3. Read the installed skill and begin its guided setup. Save personal setup answers in a private workspace outside the installed package. Resume existing answers if present.
4. If the host needs a new turn/session to discover the skill, say so. Do not claim installation or setup succeeded without checking. Surface real permission/authentication requests in plain language.
5. Installation authorizes installing this skill. It does not activate reminders, connect business accounts, contact workers, purchase services or deploy a hosted application. Those decisions belong in setup.

### Optional agent-side fallback

If no built-in skill installer is available, Codex can clone this repository, inspect the files and run `install.py` itself using an available Python 3.9+ runtime. The person should not need to operate a terminal.

The fallback copies only `skills/job-checklists` into `~/.agents/skills/job-checklists`, refuses an existing installation, and does not modify Codex settings or start automation. An agent can supply `--destination` for the host's actual skill directory. The normal built-in installer may use `$CODEX_HOME/skills` instead; use the active host's conventions.

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
