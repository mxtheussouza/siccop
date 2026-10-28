import { readFileSync } from "node:fs";
import assert from "node:assert/strict";
import test from "node:test";

test("shared TypeScript configuration enforces strict checks", () => {
  const { compilerOptions } = JSON.parse(
    readFileSync(new URL("../typescript/base.json", import.meta.url), "utf8"),
  );
  assert.equal(compilerOptions.strict, true);
  assert.equal(compilerOptions.noUncheckedIndexedAccess, true);
  assert.equal(compilerOptions.skipLibCheck, false);
});
