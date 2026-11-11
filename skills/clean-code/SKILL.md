---
name: clean-code
description: "Write readable, reusable code and focused tests during feature implementation, bug fixes, and scoped cleanup. Follow repository conventions."
---

# Clean Code

Write idiomatic code that is easy to understand and maintain. Apply this guidance across languages, adapting to repository conventions and the user's requested scope.

## Language guidance

When working in these languages, read the relevant guide for idioms, testing choices, and worked examples. For mixed-language changes, consult the guides for the code being changed. Use the repository's existing tools and conventions; the examples illustrate decisions, not required frameworks.

- [Go](references/go.md): error contracts, ownership, interfaces, and isolated tests.
- [TypeScript](references/typescript.md): type narrowing, async contracts, and deterministic tests.
- [Python](references/python.md): shared behavior, resource ownership, fixtures, and patch boundaries.
- [Bash](references/bash.md): quoting, exit status, pipelines, and script tests.

## Find and reuse existing behavior

- Before introducing a helper, component, type, or dependency, inspect nearby implementations and callers. Use `rg` or the available repository search to look for the responsibility as well as likely names. Reuse a suitable maintained implementation when its contract fits.
- Before consolidating similar code, compare inputs, outputs, validation, defaults, errors, and side effects. Account for ordering, state, and resource ownership when relevant. Similar names or text alone do not establish equivalence.
- When callers implement the same responsibility and contract, consolidate the shared behavior and update the relevant callers. Keep intentional contract differences explicit; share only the common part when that produces a clear boundary.

## Choose the simplest useful structure

- Place shared logic in the module that owns the responsibility or the nearest appropriate shared layer. Prefer cohesive, purpose-specific helpers with explicit dependencies. Avoid catchall utility modules and imports that create cycles or couple unrelated features.
- Build abstractions around demonstrated needs. Avoid speculative frameworks, configuration switches, or new dependencies introduced solely to remove a few repeated lines. Keep small repetition when sharing would obscure behavior or add coupling; use judgment rather than a fixed repetition threshold.
- Use names that communicate intent, direct control flow, and focused responsibilities. Extract a helper when it clarifies a meaningful operation or enables real reuse. Use comments for non-obvious intent and constraints, without imposing arbitrary function-size limits.

## Write useful, readable tests

- Name the behavior and keep important inputs and expected results visible. Share setup when it clarifies the scenario; keep small repetition when a helper would hide it. Use table-driven cases when setup and assertions share a clear structure.
- Assert observable results, errors, and side effects. Check internal interactions when the interaction itself is part of the contract. Keep expected values independent of the production calculation, and make assertion failures explain what went wrong.
- Isolate mutable fixtures and control time, randomness, asynchronous completion, and external services at the relevant boundary. Prefer explicit synchronization to sleeps and small test doubles to recreating an entire dependency graph.
- Cover meaningful boundaries and failure paths in proportion to the change. Several assertions can describe one coherent outcome. For a bug fix, verify that the regression test catches the original defect when practical; distinguish blocked validation from a passing test.

## Preserve scope and verify

- Limit cleanup to touched code and duplication directly related to the task. Flag wider opportunities separately. Preserve public contracts during structural refactoring, and distinguish intentional behavior changes from behavior-preserving consolidation.
- Inspect affected callers and the final diff for stale duplicate implementations, unnecessary abstractions, and unintended behavior changes.
- Run relevant existing tests and repository-required checks. Add focused regression coverage when consolidation puts meaningful behavior at risk, including callers with distinct edge cases. Match validation to the change; do not add tests merely to mirror implementation details.
