# Sync agent skills

Keep locally installed Codex skills synchronized with this repository's `main` branch.

| Setting | Value |
| --- | --- |
| Name | Sync agent skills |
| Schedule | Every day at 9:00 AM |
| Timezone | America/New_York |
| Destination | An existing local Codex chat |
| Source | `porthorian/agent-skills`, branch `main` |

## Set up

Open a local Codex chat with access to the repository and your local skills directory, then ask:

> Create or update an active schedule named "Sync agent skills" in this chat. Run it every day at 9:00 AM America/New_York using the task prompt below. Update an existing matching schedule rather than creating a duplicate.

The active schedule is managed in the app; this file stores its reusable settings and prompt. Keep the computer on and the app running for local file access. See the [official scheduled-task documentation](https://learn.chatgpt.com/docs/automations).

## Task prompt

```text
Keep local Codex skills synchronized with the latest main branch of porthorian/agent-skills. Keep this daily schedule active after successful runs.

Resolve <codex-home> from the existing CODEX_HOME environment variable, defaulting to ~/.codex when unset. Use <codex-home>/skills for installed packages and <codex-home>/skill-sync-backups for backups and the sync receipt.

Use a fresh temporary checkout of git@github.com:porthorian/agent-skills.git on main and record the fetched commit SHA. Preserve the user's working checkout, its branch, tracked files, uncommitted work, and Git metadata. A failed or incomplete fetch or an empty source catalog is a failure, not evidence that local skills are current. Prefer git; before any gh invocation, read and follow the environment's GitHub CLI access guidance, including the github-cli-elevated skill when available. Use authorized elevated network and filesystem access when required. If access is denied, report the exact blocker without claiming synchronization succeeded.

Discover every direct skills/<name>/ directory containing SKILL.md in the fetched revision. Install new packages and synchronize existing repo-managed packages into <codex-home>/skills/<name>/. The fetched repository is authoritative for complete package contents and file modes. Stage and verify all changed packages outside the local skills discovery directory before installing them. Before replacing a differing local package, preserve its complete existing directory at <codex-home>/skill-sync-backups/<unique-UTC-timestamp>/<name>/. Retain backups until the user removes them. Replace complete packages so obsolete files within them disappear. Preserve a recoverable original if replacement fails. Recheck local contents before replacing them so concurrent edits are not silently lost. Report unsupported symlinked source packages or destinations instead of writing through them.

Preserve unrelated local skills, .system, and plugin-managed skills. Read <codex-home>/skill-sync-backups/latest-sync.json from the most recent successful run; if absent, start with an empty managed-skills history. Its managed_skills list tracks packages previously owned by this repository. If a previously managed package disappears from the repository, retain its local directory and report the removal for review; do not delete it. Preserve historical managed names in subsequent receipts so retained removed packages remain identifiable.

Verify installed package paths, file bytes, and modes against the fetched revision. Verify every replacement backup matches its pre-sync package and unrelated local entries remain unchanged. Perform a second comparison that finds no drift. Only after all verification succeeds, atomically update latest-sync.json with the repository, branch, fetched revision, completion time, current source_skills and historical managed_skills, retained_removed_skills, updates, backup locations, package fingerprints, and verification results. On partial failure, keep backups and report which updates completed without writing a successful receipt. Clean up only temporary resources created by this run.

Stay quiet when everything is already synchronized and nothing new requires attention. Report newly installed or updated skills with the fetched revision and backup locations, newly removed repo packages retained locally, or failures requiring user attention. Do not repeat unchanged findings on subsequent runs.
```
