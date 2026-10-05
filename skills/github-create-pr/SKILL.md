---
name: github-create-pr
description: "Use whenever the user asks to create or open a GitHub pull request (PR), including as part of a larger implementation task. Follow repository PR templates exactly and include test evidence that CI does not cover. Also use for PR title/body updates."
---

# Create GitHub PR

Produce a concise title and description grounded in the change, following the repository's PR template and including additional test evidence beyond CI. Publish when requested; otherwise return the proposed text.

## When to use

Apply this skill whenever the user's task asks for a GitHub PR to be created, opened, made, raised, or submitted. Requests such as "create a PR," "open a pull request," "turn this into a PR," and "implement this and open a PR" select this skill without requiring the user to name it. Also apply it to requests to update PR titles or descriptions.

Apply it to the PR portion of a broader task even before the branch is committed or pushed. Prerequisite implementation and Git work remains with the surrounding authorized workflow; the branch's current state does not prevent selecting this skill.

## Establish the change

Read the request, applicable repository instructions, actual diff, and relevant task or ticket context. Locate and read the applicable PR template before drafting, including the selected template when several are available. For an existing PR, read its current title, body, base/head branches, head commit, and available checks. Ask only when competing repositories, branches, templates, or requirements cannot be resolved from accessible context.

For publication, describe the pushed head represented by the PR. Keep unpushed local work out of claims about that head. If creating the PR requires committing or pushing, prepare the title and description and identify that prerequisite. This skill does not stage, commit, push, implement changes, or expand the surrounding task's authorization.

Gather actual test commands, results, captured output, and associated logs from the current task and saved artifacts. Identify which revision or environment a result covers when it affects interpretation. A previous description's assertion that tests passed is not captured output. Do not invent missing evidence or rerun tests solely to reconstruct missing logs.

## Follow the PR template

Treat the applicable template as the required structure. Preserve its headings, order, checklist wording, and required fields; fill them according to its instructions. Do not replace it with a stock format or add sections. If it specifically requests CI results or a complete test list, answer accurately at the requested level of detail. A generic Testing field still uses the evidence selection below.

Place additional test evidence in an existing suitable testing or validation field, using expandable logs only where its format permits. If there is no suitable field, keep the template intact and provide the additional evidence in chat. For a title-only or other narrow edit, preserve unrelated body text and metadata.

Without a template, write a concise description and add Testing only when there is additional evidence or a concrete relevant validation gap. Omit the section when there is nothing beyond CI to report.

## Select evidence beyond CI

Inspect the applicable CI workflows and the scripts, flags, test suites, and environments they invoke before choosing evidence for the description. Follow invoked targets or scripts far enough to establish coverage; compare the actual coverage rather than command names alone.

- Omit local commands, results, and logs that duplicate CI coverage. A local run with materially different flags, scope, or environment can add evidence, such as race detection absent from CI or a distinct integration or hardware test. Include it when that difference helps assess the change.
- Coverage means what the applicable CI workflow is responsible for. A pending, failed, or skipped run does not automatically turn a routine duplicate check into additional testing.
- Omit CI status recaps and CI logs from the description unless the template explicitly requests them. Leave those results in GitHub Checks and report material CI problems briefly in chat.
- When CI coverage cannot be established, retain relevant local evidence and explain the coverage uncertainty in chat. Do not assume a test is duplicated without evidence.
- Keep concrete gaps in additional validation brief. Avoid hypothetical test inventories, operational disclaimers, and a general rollout checklist.

## Write the title and description

Use a concise title describing the resulting change and follow repository title conventions. Explain the concrete problem and resulting behavior in the appropriate template field, or early in the description when there is no template. Include rationale or implementation details when they help reviewers assess the change. Scale length to complexity while preserving the template's structure.

Describe the final implementation for someone who has not read the conversation. Remove stale scope, abandoned approaches, and work-session narration unless a tradeoff matters to review.

Avoid dense "Validation: everything passed" paragraphs. Measurements and environment output for selected additional tests belong in the permitted log format rather than a narrative recap. Omit boilerplate about actions not performed, operator ownership, deployment boundaries, handoffs, and future PRs. State concrete gaps in additional validation briefly, without surrounding defensive commentary. Include a compatibility or behavior limitation only when it explains the change or affects a review decision.

Use plain, specific prose and regular ASCII hyphens in ordinary text. Preserve punctuation in exact output, code, quotations, official names, and required templates. Self-review the proposed text against the diff and evidence for factual accuracy, useful detail, repetition, unsupported claims, and the writing rules above.

## Present the selected test evidence

- List each selected command actually run with its observed result. Use labels such as passed, failed, or interrupted; do not turn a missing result into a pass.
- Include captured stdout/stderr and associated logs. When the template permits, or when there is no template, use fenced code blocks inside expandable `<details>` sections with meaningful `<summary>` labels. Otherwise follow its prescribed format. Keep blank lines around fenced blocks and use a longer fence when output contains backticks.
- Identify a different test scope or environment briefly when it explains why the evidence adds coverage beyond CI. Keep relevant results from earlier revisions or superseded failures identifiable; do not present them as results for the current head.
- For oversized output, link to existing accessible log artifacts and include a useful excerpt. Identify truncation or unavailable output briefly. Do not invent an artifact URL or upload logs to another service as part of this skill.
- Redact secrets and unrelated sensitive data from output, log excerpts, artifact links, and descriptions before publishing. Mark redactions without changing the meaning of the result.

Use the following shape only when there is no template and additional evidence warrants a Testing section. The placeholders illustrate structure; replace them only with observed evidence.

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

For a selected test whose result is known but whose output was not retained, list the result with "Output unavailable." Do not manufacture a representative transcript. Include available associated logs in the same block or separate labeled blocks. Preserve consequential failures even when omitting unrelated noise from an oversized log.

## Publish and verify

A request to create or update a PR authorizes publishing the requested title and body without another confirmation. Honor requests for proposed text only, read-only work, or narrower edits. Opening a PR does not authorize merging it, changing code, posting review feedback, or adding reviewers or labels.

Before any `gh` invocation, read and follow the environment's GitHub CLI access guidance, including the `github-cli-elevated` skill when available. Use available GitHub tools or non-interactive CLI calls with explicit repository, base/head branches, title, and body as appropriate. Avoid interactive flows that offer to commit or push. Pass multiline bodies through structured arguments or a temporary file with `--body-file`, preserving literal text and newlines.

Establish the repository and intended base/head branches and look for an existing open PR before creating one. Update a matching PR rather than creating a duplicate when the request covers it. Open new PRs ready for review by default and honor an explicit draft request. Preserve an existing PR's draft status and unrelated metadata during text edits.

Refresh the relevant PR/head state before writing. If it has changed, reconcile the description and test evidence with the current change. After writing, read back the title, body, branches, and status and verify the requested result. If a write times out or has an uncertain outcome, inspect the existing PR before retrying; do not blindly create another PR or overwrite concurrent edits. If the outcome cannot be established, return the proposed text and report the uncertainty instead of retrying.

Return the PR link, or the proposed title and description when publication was not requested or could not be completed. Report any unresolved access or verification gap briefly in chat. Attach every created PR to the current Codex chat using the artifact attachment tool when supported.
