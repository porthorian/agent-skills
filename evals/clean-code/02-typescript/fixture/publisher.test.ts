import test from "node:test";
import assert from "node:assert/strict";
import { publish } from "./publisher.ts";

test("returns the trimmed topic", async () => {
  const writer = { async write(_topic: string): Promise<void> {} };
  assert.equal(await publish(writer, " updates "), "updates");
});
