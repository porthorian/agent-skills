# TypeScript

Keep the project's runtime, compiler settings, and test framework. The examples use erasable TypeScript and Node's test APIs to keep dependencies small, not to prescribe a framework.

- Model meaningful states with types and narrow them at use sites. Validate untrusted runtime data at the boundary; a type assertion does not validate it. Avoid widening to `any` to make an abstraction fit.
- Make async completion and rejection part of the function's contract. Await work the caller depends on; make ownership and failure handling explicit for intentionally detached work.
- Await or return test promises. Use a controlled dependency or deferred promise to exercise completion ordering; use fake clocks when the behavior actually depends on time. Assert useful values or effects, with interaction assertions for contractual calls. Follow existing UI test conventions for user-visible behavior.

## Implementation: narrow a meaningful state

Both versions use this union:

```typescript
type Job =
  | { state: "ready"; id: string }
  | { state: "waiting"; retryAt: number };
```

Before:

```typescript
function readyId(job: Job): string | undefined {
  return (job as { id?: string }).id;
}
```

After:

```typescript
function readyId(job: Job): string | undefined {
  return job.state === "ready" ? job.id : undefined;
}
```

The discriminant explains which state owns an ID and lets the compiler check that access. A local condition is sufficient here; adding a generic state-selection framework would obscure the decision. Boundary validation would still be needed if the value came from untrusted JSON.

## Testing: wait for the result and keep the dependency small

The function under test is:

```typescript
async function displayName(load: () => Promise<{ name: string }>): Promise<string> {
  const account = await load();
  return account.name.trim();
}
```

Both tests use `import test from "node:test"` and `import assert from "node:assert/strict"`.

Before:

```typescript
test("display name", () => {
  displayName(async () => ({ name: " Ada " })).then((name) => {
    assert.equal(name, "Ada");
  });
});
```

After:

```typescript
test("returns the loaded name without surrounding whitespace", async () => {
  const name = await displayName(async () => ({ name: " Ada " }));
  assert.equal(name, "Ada");
});
```

The test runner can track completion and failure, the expected value is explicit, and the fake supplies exactly the external result the test needs. If the requirement were that a write finishes before resolution, use a controlled pending write and observe completion before releasing it. This value-only test would not establish that ordering contract. Keep an integration test for any real transport behavior that matters.

See [TypeScript narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html) and [Node's test runner](https://nodejs.org/api/test.html).
