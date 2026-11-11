# Python

Follow the project's Python version and testing conventions; use its existing pytest or unittest style. The examples use the standard library.

- Keep data flow explicit and use context managers for owned resources. Prefer straightforward functions and data structures to a new class hierarchy or framework for a small operation.
- Share behavior only after comparing defaults, exceptions, encodings, and ownership. Avoid mutable default arguments when calls need independent state. Fixture scope should match the intended sharing; make behavior-relevant fixture values and overrides visible.
- Patch a dependency where the code under test looks it up. Use scoped patches and an appropriate spec when a mock is needed. Keep ordinary transformations real, and substitute external boundaries without contacting live services. Assert calls when those calls are the behavior being promised.

## Implementation: share the operation that has the same contract

Both readers own the file, decode UTF-8 JSON, and propagate the same read and decode exceptions. Both versions use `json`.

Before:

```python
def read_limits(path):
    with open(path, encoding="utf-8") as source:
        document = json.load(source)
    return document["limits"]


def read_features(path):
    with open(path, encoding="utf-8") as source:
        document = json.load(source)
    return document["features"]
```

After:

```python
def _read_json(path):
    with open(path, encoding="utf-8") as source:
        return json.load(source)


def read_limits(path):
    return _read_json(path)["limits"]


def read_features(path):
    return _read_json(path)["features"]
```

The shared helper owns one complete operation; the callers retain their field selection. Keep separate paths when their encodings, exception translation, streaming behavior, or resource ownership differ. A caller-owned open stream would require a different boundary.

## Testing: patch the lookup boundary and assert the outcome

In `notifications.py`, `from gateway import deliver` binds the dependency locally:

```python
def notify(address):
    return deliver(address, "ready")
```

The tests below use `unittest`, `from unittest.mock import patch`, and `import notifications`. `gateway.deliver` is an external boundary; sending the address and message is part of `notify`'s contract.

Before:

```python
class NotifyTests(unittest.TestCase):
    @patch("gateway.deliver")
    def test_notify(self, deliver):
        self.assertTrue(callable(notifications.notify))
```

After:

```python
class NotifyTests(unittest.TestCase):
    def test_delivers_ready_message_and_returns_receipt(self):
        with patch("notifications.deliver", autospec=True, return_value="sent") as deliver:
            receipt = notifications.notify("reader@example.test")

        self.assertEqual(receipt, "sent")
        deliver.assert_called_once_with("reader@example.test", "ready")
```

The original test never exercises the function, and its patch targets a different binding. The revised test checks a returned value and the promised boundary interaction, restoring the patch afterward. For code that already accepts a transport dependency, pass a small fake instead of adding a patch. Use a real fixture when reading or transforming local data is the behavior under test.

See Python's documentation on [where to patch](https://docs.python.org/3/library/unittest.mock.html#where-to-patch).
