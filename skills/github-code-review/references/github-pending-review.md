# Pending GitHub review operations

Read this reference when a review involves GitHub. Use GitHub CLI API calls under the environment's applicable access guidance. When saving feedback to GitHub, keep it pending unless the user explicitly requests publication.

The normal draft writes are:

- REST `POST repos/{owner}/{repo}/pulls/{number}/reviews`, with the reviewed `commit_id` and inline comments, **omitting `event`**.
- GraphQL `addPullRequestReviewThread` with an explicit, verified pending `pullRequestReviewId`, to append to an existing compatible draft.

`gh pr review`, `gh pr comment`, standalone REST review-comment creation, and review-submission mutations are not draft substitutes. They can publish feedback immediately. Explicit publication is a separate user-authorized operation; the overall recommendation remains in chat by default.

## Preflight and identity

When using Codex's `exec_command` tool, run every `gh` command, including read-only and authentication checks, with `sandbox_permissions: "require_escalated"` and a purpose-specific justification. If access is denied, report the blocked action and reason without retrying in the default sandbox. Elevated credential access does not authorize GitHub writes.

Resolve the exact GitHub host, repository, PR number, authenticated reviewer, and reviewed head SHA. Honor the repository's configured host; use `--hostname` for enterprise hosts rather than assuming github.com. Never print tokens or initiate authentication changes as part of a review.

Through `gh api`, read:

1. `user` to identify the authenticated reviewer.
2. `repos/{owner}/{repo}/pulls/{number}` for the PR author in `user`, PR state, `head.sha`, `base.sha`, and identity.
3. The current PR diff, plus all pages of reviews, review comments, and conversation comments.
4. The authenticated reviewer's pending review and its comments, if one exists. GraphQL review threads expose resolved/outdated state when needed for deduplication.

Before any creation or append, compare the PR author's identity with the authenticated account for the same host. If they match, report findings in chat and preserve existing reviews and comments; save pending feedback only when explicitly requested. A known different author uses the normal pending-comment default even when the authenticated user owns the repository. If either identity is unavailable or authorship remains ambiguous, report the limitation and findings in chat without GitHub writes until identity is established. Prefer account IDs when present; otherwise compare logins case-insensitively. Repository ownership is not PR authorship.

Relevant REST reads:

```text
GET repos/{owner}/{repo}/pulls/{number}/reviews
GET repos/{owner}/{repo}/pulls/{number}/comments
GET repos/{owner}/{repo}/issues/{number}/comments
GET repos/{owner}/{repo}/pulls/{number}/reviews/{review_id}
GET repos/{owner}/{repo}/pulls/{number}/reviews/{review_id}/comments
```

Use `--paginate` for REST lists and follow GraphQL connection cursors, including nested comment pages when needed. Reading only the first page can miss the existing draft or duplicate feedback.

Require an open PR and a head matching the reviewed snapshot before writing. Match an existing draft to the authenticated author, `PENDING` state, and reviewed commit. A draft pinned to an older or unknown commit is incompatible: preserve it and keep new feedback in chat. Do not delete, submit, or recreate the user's draft to get around this condition.

## Select new comments and valid anchors

Compare candidate feedback with existing pending and submitted discussion, including bot feedback. Deduplicate by the underlying issue and requested action, not wording alone. A resolved discussion does not automatically prove the current code is correct; assess whether new behavior or evidence actually warrants new substance.

Use repository-relative `path` and verified diff lines:

- `RIGHT` refers to the new/head file; `LEFT` refers to the old/base file.
- `line` is a file line number on that side, not a diff-position count.
- For multiline comments, `start_line`/`start_side` identify the beginning and `line`/`side` identify the end. Keep the range small and valid in the reviewed diff.

Local-only or unpushed lines are not valid PR anchors. Keep unanchorable findings in chat. Do not fall back to the standalone comments endpoint to avoid a draft-review or anchor error.

## Create one pending review

Write a JSON request file using a serializer. Preserve actual newlines and literal text; use `--input` rather than interpolating bodies into shell commands. Leave out `event` entirely and leave out `body` by default because the summary belongs in chat.

Example payload, with illustrative identifiers to replace from the current PR:

```json
{
  "commit_id": "REVIEWED_HEAD_SHA",
  "comments": [
    {
      "path": "src/allocator.go",
      "line": 42,
      "side": "RIGHT",
      "body": "If the reservation has expired, this path can reuse an allocation that has already been reassigned. Could we re-check ownership and cover that sequence with a regression test?"
    }
  ]
}
```

After a final fresh head/draft check, invoke through an elevated `exec_command`:

```sh
gh api --method POST repos/OWNER/REPO/pulls/NUMBER/reviews --input /absolute/path/pending-review.json
```

Batch new comments in the single creation request. Do not create an empty review when there is no actionable feedback.

Inspect the response, retain the review ID and node ID, then read the review and its complete comments back. Require:

- `state` is `PENDING`.
- `submitted_at` is absent or null.
- The review author and `commit_id` match the expected reviewer and reviewed head.
- Each expected comment exists exactly once with the expected body and an appropriate anchor.

Read the PR head again after saving. A success response alone does not establish that the draft is complete, correctly anchored, or current.

## Append to an existing compatible draft

Preserve the review body and all earlier comments. Use its node ID explicitly; do not use a mutation that may implicitly choose or create a review.

Serialize the following GraphQL operation and variables to a JSON request file:

```graphql
mutation AppendPendingThread($input: AddPullRequestReviewThreadInput!) {
  addPullRequestReviewThread(input: $input) {
    thread { id }
  }
}
```

```json
{
  "query": "mutation AppendPendingThread($input: AddPullRequestReviewThreadInput!) { addPullRequestReviewThread(input: $input) { thread { id } } }",
  "variables": {
    "input": {
      "pullRequestReviewId": "VERIFIED_PENDING_REVIEW_NODE_ID",
      "path": "src/allocator.go",
      "line": 42,
      "side": "RIGHT",
      "body": "The specific scenario and consequence. Could we cover this case?"
    }
  }
}
```

Use `startLine` and `startSide` for a multiline GraphQL range. GraphQL field names use camel case; REST uses snake case.

```sh
gh api graphql --input /absolute/path/append-pending-thread.json
```

Append sequentially. Before each mutation, re-check the current head, the draft's pending state, author, and commit, and that the comment has not already appeared. A human may have submitted or edited the draft since preflight. After each mutation, inspect GraphQL `errors` even when HTTP succeeds, then read the review and comments back and verify the pending state, new comment, and preserved earlier content. Read the head again before proceeding.

## Changes, failures, and uncertain results

- If the head changes before the first write, refresh and re-review affected behavior and anchors. If it changes again during saving, stop further writes and report the reviewed and current heads and any saved comments; preserve existing drafts.
- If a creation or append request times out, fails, returns GraphQL errors, or has an incomplete response, stop mutations and read back the pending review and comments. When creation returns no review ID, discover the pending review through the review list and inspect only IDs returned by GitHub. Do not assume failure means no comment was saved, and do not blindly repeat a non-idempotent write.
- Once read-back establishes what was saved and verifies pending state, identity, and commit compatibility, the next distinct candidate may proceed. Retry the same candidate only after read-back proves it absent. If outcome, identity, or compatibility remains uncertain, leave remaining feedback in chat and report the limitation.
- If elevation, authentication, or authorization fails, follow the applicable access guidance. Do not switch to another transport or credential source to bypass the denial.
- If a draft was submitted concurrently or becomes incompatible, stop additions and report the state. Never reverse the submission, delete comments, or create a replacement draft automatically.
- If verification exposes unexpected publication, stop immediately and tell the user what occurred. Do not attempt an unauthorized deletion or dismissal.

For legacy responses where a comment's `line` is null, inspect its commit, `original_line`, `diff_hunk`, and available position/range information to establish the actual anchor. A null `line` by itself is neither proof of failure nor proof of correct placement. If placement cannot be established, report it as unverified.

## Report verified state

Return the review URL and comment URLs GitHub provides. If a response lacks a URL, derive it only from a verified repository/PR and returned review or comment ID. Report the number of comments verified as pending, identify unsaved or unverified findings, and separate draft persistence from validation of the code itself. Keep the ready/hold/inconclusive recommendation and test report in chat.

## Authoritative references

- [REST pull request reviews](https://docs.github.com/en/rest/pulls/reviews#create-a-review-for-a-pull-request): creation with no `event`, pending state, review reads, and comment lists.
- [GraphQL pull request operations](https://docs.github.com/en/graphql/reference/pulls#addpullrequestreviewthread): adding a thread to a pending review using its ID.
- [GitHub CLI API](https://cli.github.com/manual/gh_api): JSON request files, pagination, hosts, and GraphQL calls.
