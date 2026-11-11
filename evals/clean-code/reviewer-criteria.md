# Reviewer criteria

Keep this file out of worker prompts. Inspect the resulting files and actual test output; a worker's statement that it followed the skill is not evidence by itself. Judge against the task's contract, allowing different correct implementations.

## Shared dimensions

- **Correctness:** The requested behavior works and the relevant checks pass.
- **Contracts:** Existing promised inputs, outputs, exceptions, side effects, and ownership remain intact except for the requested correction.
- **Tests:** Added tests exercise the behavior, expose important inputs and independent expectations, and avoid unnecessary nondeterminism or hidden shared state. For bug fixes, the tests detect the original defect where practical. Existing tests remain meaningful.
- **Structure:** Reuse follows matching responsibilities and contracts; helpers clarify real operations. Small intentional repetition is acceptable. More extraction is not automatically better.
- **Scope:** Edits stay within the requested task. Explanation-only requests leave all fixture files unchanged.

## 01-go

- Upstream error identity survives `LookupLabel`; contextual text still includes `lookup label:`. Successful values are still trimmed, and the public signature is unchanged.
- A test uses an independent sentinel or typed error and a causal assertion such as `errors.Is`, and fails against the original `%v` implementation. It also retains coverage of successful trimming.
- Fixtures have no shared mutable state; parallelization and new dependencies are unnecessary. Exact platform error wording is not required.

## 02-typescript

- `publish` trims the topic, waits for `write`, returns the trimmed topic on success, and propagates a write rejection.
- A deterministic completion test controls a pending write and observes that publication remains pending before releasing it. A rejection test is awaited. Assert the written value as well as the return value where relevant.
- Tests detect the original detached write without arbitrary sleeps, live services, or an unobserved assertion inside an unreturned promise.

## 03-python

- Calls without `history` get independent lists. A supplied list is appended to and returned as the same object, including an initially empty supplied list. Transport errors continue to propagate.
- Tests patch the lookup in `notifier` or use another justified local substitution. They assert independent calls and explicit-list behavior without contacting the failing transport stub.
- The new tests fail against the original mutable default and do not pass accidentally because earlier tests cleared shared state.

## 04-bash

- `snapshot` copies bytes between paths containing spaces, emits `saved` on success, and returns the failing copy command's status without a success message on failure. The script remains sourceable.
- Tests check bytes, stdout, stderr, and status. A controlled `cat` failure with a recognizable nonzero status can verify exact propagation; a missing-file test alone establishes only a nonzero result.
- Expected failures are handled explicitly in the test harness. Scratch files use the supplied artifact directory; no external service or platform-specific error text is needed.

## 05-reuse

- `preview_job` reuses the maintained `parse_region` behavior rather than growing a parallel implementation. Both job paths normalize whitespace/case and reject blank regions with the canonical error.
- Response shapes remain distinct and unchanged. Focused tests include a noncanonical region and blank input, with explicit expected values.
- The shared normalization retains its owner; a generic new utility layer is unnecessary.

## 06-contracts

- Limits default to 100 and allow integers from 1 upward; retries default to 0 and allow integers from 0 upward. `None` and the empty string use each function's default. Invalid integers still raise `ValueError`; no new coercion policy is introduced.
- The distinct validation messages and valid zero-retry case remain intact. A small helper is acceptable if it shares only truly common behavior and leaves policies visible. Keeping the functions separate is also acceptable.
- Tests cover distinct defaults, zero, negative values, and malformed integers. The change does not invent upper bounds, switches, or a parsing framework.

## 07-explanation

- Explains that display labels preserve case while lookup keys are case-insensitive, using examples that distinguish their outputs.
- Explains a reasonable sharing boundary without claiming similar text proves equivalent contracts.
- All fixture files remain byte-for-byte unchanged; creating a helper, tests, or cache files in the fixture fails scope. There is no required code change or test run.
