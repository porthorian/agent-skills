# Go

Use the module's supported Go version and established test style.

- Preserve error contracts. Wrap with `%w` when callers need to inspect an underlying error; use `errors.Is` or `errors.As` for that contract. Match exact text when the text is itself a promised output.
- Keep resource and goroutine ownership clear: who closes, cancels, and waits? Prefer small interfaces at the consumer boundary when they describe a real dependency; avoid introducing an interface for every concrete type.
- Use named table cases when cases share setup and assertions. Mark test helpers with `t.Helper()` and register owned-resource cleanup with `t.Cleanup()` or the appropriate test helper. Parallel tests need independent state; process-wide environment changes and shared mutable fixtures need particular care.

## Implementation: keep the underlying error inspectable

Both versions below use `fmt` and `os`. The config caller needs to recognize a missing file while retaining context. The summary boundary promises contextual text but does not expose its underlying error for inspection.

Before:

```go
func readConfig(path string) ([]byte, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("read config: %v", err)
    }
    return data, nil
}

func readSummary(path string) ([]byte, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("read summary: %v", err)
    }
    return data, nil
}
```

After:

```go
func readConfig(path string) ([]byte, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("read config: %w", err)
    }
    return data, nil
}

func readSummary(path string) ([]byte, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("read summary: %v", err)
    }
    return data, nil
}
```

The change deliberately exposes the config error to `errors.Is` and `errors.As` while preserving the summary contract. Keep the small repeated read rather than adding a wrapper with switches for these different error policies. Wrapping an internal dependency's error can make it part of the public contract; consolidate only when the callers actually share that policy.

## Testing: assert the error contract with an isolated fixture

These tests use `testing`; the revised test also uses `errors`, `io/fs`, and `path/filepath` and tests the revised `readConfig` above.

Before:

```go
func TestReadConfigMissing(t *testing.T) {
    _, err := readConfig("missing")
    if err == nil || err.Error() != "read config: open missing: no such file or directory" {
        t.Fatalf("unexpected error: %v", err)
    }
}
```

After:

```go
func TestReadConfigMissing(t *testing.T) {
    path := filepath.Join(t.TempDir(), "missing.json")
    _, err := readConfig(path)
    if !errors.Is(err, fs.ErrNotExist) {
        t.Fatalf("readConfig(%q): got %v, want a missing-file error", path, err)
    }
}
```

The revised test owns its directory and checks the promised cause without depending on OS wording. Separate cases would be clearer than a table when each case needs substantially different resource setup. Add `t.Parallel()` only when the fixture and dependencies actually permit it.

See the Go documentation on [error wrapping](https://go.dev/blog/go1.13-errors) and [table-driven tests](https://go.dev/wiki/TableDrivenTests).
