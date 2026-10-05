---
name: github-create-pr
description: "Use whenever the user asks to create or open a GitHub pull request (PR), including as part of a larger implementation task. Write concise titles and descriptions with captured test output and logs. Also use for PR title/body updates."
---

# Create GitHub PR

Produce a clear title and description grounded in the change, with direct test evidence. Publish when requested; otherwise return the proposed text.

## When to use

Apply this skill whenever the user's task asks for a GitHub PR to be created, opened, made, raised, or submitted. Requests such as "create a PR," "open a pull request," "turn this into a PR," and "implement this and open a PR" select this skill without requiring the user to name it. Also apply it to requests to update PR titles or descriptions.

Apply it to the PR portion of a broader task even before the branch is committed or pushed. Prerequisite implementation and Git work remains with the surrounding authorized workflow; the branch's current state does not prevent selecting this skill.

## Establish the change

Read the request, applicable repository instructions, actual diff, relevant task or ticket context, and selected PR template. For an existing PR, read its current title, body, base/head branches, head commit, and available checks. Ask only when competing repositories, branches, templates, or requirements cannot be resolved from accessible context.

For publication, describe the pushed head represented by the PR. Keep unpushed local work out of claims about that head. If creating the PR requires committing or pushing, prepare the title and description and identify that prerequisite. This skill does not stage, commit, push, implement changes, or expand the surrounding task's authorization.

Gather the actual test commands, results, captured output, and associated logs from the current task, saved artifacts, and relevant CI runs. Identify which revision or environment a result covers when it affects interpretation. A previous description's assertion that tests passed is not captured output. If task or test evidence is unavailable, state the specific gap rather than inventing it. Do not rerun tests solely to reconstruct missing logs.

## Write the title and description

Use a concise title describing the resulting change and follow repository title conventions. Explain the concrete problem and resulting behavior early in the description. Include rationale or implementation details when they help reviewers assess the change. Scale length and structure to complexity and honor the selected repository template.

Describe the final implementation for someone who has not read the conversation. Remove stale scope, abandoned approaches, and work-session narration unless a tradeoff matters to review. For a title-only or other narrow edit, preserve unrelated text and metadata rather than rewriting the whole PR.

Avoid dense "Validation: everything passed" paragraphs. Detailed validation measurements, fixture inventories, and environment output belong in expandable test logs rather than a narrative recap. Omit boilerplate about actions not performed, operator ownership, deployment boundaries, handoffs, and future PRs. Keep concrete, relevant failed, skipped, or incomplete validation in Testing, such as "Production canary: incomplete," without surrounding defensive commentary. Include a compatibility or behavior limitation only when it explains the change or affects a review decision.

Use plain, specific prose and regular ASCII hyphens in ordinary text. Preserve punctuation in exact output, code, quotations, official names, and required templates. Self-review the proposed text against the diff and evidence for factual accuracy, useful detail, repetition, unsupported claims, and the writing rules above.

## Include Testing

Every complete description includes Testing. Use the repository template's equivalent testing or validation section when present; otherwise add `## Testing`. A narrow title-only edit does not authorize adding a section to the existing body.

- List each command actually run with its observed result. Use labels such as passed, failed, or interrupted; do not turn a missing result into a pass. State when no tests were run.
- Put captured stdout/stderr and associated test logs in fenced code blocks inside expandable `<details>` sections, with a meaningful `<summary>` identifying the command or log. Keep a blank line around fenced blocks so they render correctly. Use a longer fence if the output itself contains backticks.
- Distinguish local checks, CI, and runtime evidence. Keep results from earlier revisions or superseded failures identifiable when relevant; do not present them as results for the current head.
- Include relevant failed, skipped, or incomplete checks briefly. List concrete validation gaps rather than hypothetical tests or operational disclaimers.
- For oversized output, link to existing accessible log artifacts and include a useful excerpt. Identify truncation or unavailable output briefly. Do not invent an artifact URL or upload logs to another service as part of this skill.
- Redact secrets and unrelated sensitive data from output, log excerpts, artifact links, and descriptions before publishing. Mark redactions without changing the meaning of the result.

Use the following shape when the repository template does not specify another. The placeholders illustrate structure; replace them only with observed evidence.

````markdown
## Testing

- `<command actually run>`: <observed result>.

<details>
<summary>Output: <command actually run></summary>

```text
<captured output, with any necessary redactions marked>
```

</details>
````

When a result is known but its output was not retained, list the result with "Output unavailable." Do not manufacture a representative transcript. Include available associated logs in the same block or separate labeled blocks. Preserve consequential failures even when omitting unrelated noise from an oversized log.

## Publish and verify

A request to create or update a PR authorizes publishing the requested title and body without another confirmation. Honor requests for proposed text only, read-only work, or narrower edits. Opening a PR does not authorize merging it, changing code, posting review feedback, or adding reviewers or labels.

Before any `gh` invocation, read and follow the environment's GitHub CLI access guidance, including the `github-cli-elevated` skill when available. Use available GitHub tools or non-interactive CLI calls with explicit repository, base/head branches, title, and body as appropriate. Avoid interactive flows that offer to commit or push. Pass multiline bodies through structured arguments or a temporary file with `--body-file`, preserving literal text and newlines.

Establish the repository and intended base/head branches and look for an existing open PR before creating one. Update a matching PR rather than creating a duplicate when the request covers it. Open new PRs ready for review by default and honor an explicit draft request. Preserve an existing PR's draft status and unrelated metadata during text edits.

Refresh the relevant PR/head state before writing. If it has changed, reconcile the description and test evidence with the current change. After writing, read back the title, body, branches, and status and verify the requested result. If a write times out or has an uncertain outcome, inspect the existing PR before retrying; do not blindly create another PR or overwrite concurrent edits. If the outcome cannot be established, return the proposed text and report the uncertainty instead of retrying.

Return the PR link, or the proposed title and description when publication was not requested or could not be completed. Report any unresolved access or verification gap briefly in chat. Attach every created PR to the current Codex chat using the artifact attachment tool when supported.
