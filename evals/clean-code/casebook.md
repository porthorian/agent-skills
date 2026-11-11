# Clean-code casebook

Use this small casebook when changing the skill's behavior. It is a manual comparison protocol, not an agent runner. The fixtures use local data and standard-library test tools; they have no production access. Initial tests pass but intentionally leave gaps for the task to address.

## Cases

| Case | Task input | Starting files | Test command from the working copy |
| --- | --- | --- | --- |
| 01-go | [Prompt](01-go/prompt.md) | [Fixture](01-go/fixture) | `go test ./...` |
| 02-typescript | [Prompt](02-typescript/prompt.md) | [Fixture](02-typescript/fixture) | `node --test publisher.test.ts` |
| 03-python | [Prompt](03-python/prompt.md) | [Fixture](03-python/fixture) | `python3 -m unittest -v` |
| 04-bash | [Prompt](04-bash/prompt.md) | [Fixture](04-bash/fixture) | `bash test.sh "$CASE_ARTIFACTS"` |
| 05-reuse | [Prompt](05-reuse/prompt.md) | [Fixture](05-reuse/fixture) | `python3 -m unittest -v` |
| 06-contracts | [Prompt](06-contracts/prompt.md) | [Fixture](06-contracts/fixture) | `python3 -m unittest -v` |
| 07-explanation | [Prompt](07-explanation/prompt.md) | [Fixture](07-explanation/fixture) | Read-only task; compare file contents before and after |

Use Go 1.22 or newer, Python 3.10 or newer, Bash, and a Node runtime supporting native TypeScript type stripping. The TypeScript fixture exercises runtime behavior; Node does not type-check it. Use the host repository's TypeScript check when evaluating a real project. The fixtures choose standard tools to be self-contained; they do not prescribe frameworks for other repositories.

## Replay a comparison

1. Record the baseline and candidate skill revisions or package hashes, model, reasoning settings, available tools, and runtime versions. Keep the same settings and permissions for both variants.
2. Prepare a fresh copy of each fixture for each variant under the invoking task's persistent state directory. Keep the skill packages, prompts, and reviewer criteria outside the writable fixture copies. Supply an explicit fixture/artifact destination, including `CASE_ARTIFACTS` for Bash; preserve the system `TMPDIR`.
3. Give the worker only the relevant `prompt.md`, the starting fixture, and the selected skill package. Ask it to use that package for implementation tasks. For case 07, send only its explanation request and fixture so the no-edit boundary is not diluted by implementation instructions. Do not send reviewer criteria or another run's solution. In ordinary use, read only the language guides relevant to a task.
4. Save the actual diff, final response, commands, outputs, and any blocked validation. Review against [reviewer-criteria.md](reviewer-criteria.md). Use fresh workers for each variant; record that grouping multiple cases in one worker can influence later cases.
5. Run the resulting tests. For bug-fix cases 01-04, copy the revised tests into a separate copy of the original implementation and check for the expected failure. Keep any supporting test helpers, but restore the original production files. This checks that the tests detect the defect. It does not replace inspecting the assertions.
6. Compare per-case pass/fail results with evidence. Repeat ambiguous or inconsistent results on fresh copies. A single run is directional evidence, not a reliable measured improvement. Keep correctness, contracts, useful tests, justified structure, and scope visible separately rather than hiding a regression in an aggregate score.

Use a result table with columns: case, variant, correctness, contracts, tests, structure, scope, and evidence. Mark a blocked check as blocked; mark a dimension not relevant to the task as not applicable. Do not grade exact helper names, wording, line counts, or maximum deduplication.

The [initial comparison](results/2026-11-11.md) records the baseline, candidate, environment, and observed coverage difference.

## Maintain the skill from observed behavior

After real work reveals a concrete problem, preserve a small sanitized reproduction, expected behavior, and source evidence. Session review can help identify candidates. Add a case before changing the rule or example, then compare the baseline and candidate on the same cases. Publish the supported change through a reviewable PR.

Periodically remove redundant instructions and obsolete examples, and replay the cases they protected. Preserve repository conventions and explicit user constraints. Keep run evidence in the task's persistent state directory rather than committing private logs or teaching examples copied from customer code. The reusable prompts and fixtures belong in this casebook.

This casebook evaluates behavior under supplied tasks. The core skill's automatic-invocation metadata is checked separately; case 07 checks edit scope, not whether an implicit skill selection occurred.
