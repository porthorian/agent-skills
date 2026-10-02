---
name: clean-code
description: "Write and refactor readable, reusable code with pragmatic duplication reduction. Use during feature implementation, bug fixes, and requested code cleanup; follow repository conventions and keep refactors within the task."
---

# Clean Code

Write idiomatic code that is easy to understand and maintain. Apply this guidance across languages, adapting to repository conventions and the user's requested scope.

## Find and reuse existing behavior

- Before introducing a helper, component, type, or dependency, inspect nearby implementations and callers. Use `rg` or the available repository search to look for the responsibility as well as likely names. Reuse a suitable maintained implementation when its contract fits.
- Before consolidating similar code, compare inputs, outputs, validation, defaults, errors, and side effects. Account for ordering, state, and resource ownership when relevant. Similar names or text alone do not establish equivalence.
- When callers implement the same responsibility and contract, consolidate the shared behavior and update the relevant callers. Keep intentional contract differences explicit; share only the common part when that produces a clear boundary.

## Choose the simplest useful structure

- Place shared logic in the module that owns the responsibility or the nearest appropriate shared layer. Prefer cohesive, purpose-specific helpers with explicit dependencies. Avoid catchall utility modules and imports that create cycles or couple unrelated features.
- Build abstractions around demonstrated needs. Avoid speculative frameworks, configuration switches, or new dependencies introduced solely to remove a few repeated lines. Keep small repetition when sharing would obscure behavior or add coupling; use judgment rather than a fixed repetition threshold.
- Use names that communicate intent, direct control flow, and focused responsibilities. Extract a helper when it clarifies a meaningful operation or enables real reuse. Use comments for non-obvious intent and constraints, without imposing arbitrary function-size limits.

## Preserve scope and verify

- Limit cleanup to touched code and duplication directly related to the task. Flag wider opportunities separately. Preserve public contracts during structural refactoring, and distinguish intentional behavior changes from behavior-preserving consolidation.
- Inspect affected callers and the final diff for stale duplicate implementations, unnecessary abstractions, and unintended behavior changes. Keep tests readable even when that means repetition in setup or assertions.
- Run relevant existing tests and repository-required checks. Add focused regression coverage when consolidation puts meaningful behavior at risk, including callers with distinct edge cases. Match validation to the change; do not add tests merely to mirror implementation details.
