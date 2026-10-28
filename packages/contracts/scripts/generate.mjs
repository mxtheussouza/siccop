import { spawnSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import openapiTS, { astToString } from "openapi-typescript";

const root = fileURLToPath(new URL("../../../", import.meta.url));
const result = spawnSync("uv", ["run", "--project", "apps/api", "python", "-m", "app.export_openapi"], { cwd: root, encoding: "utf8" });
if (result.error || result.status !== 0) {
  process.stderr.write(result.stderr || String(result.error));
  process.exit(result.status || 1);
}
const schema = JSON.parse(result.stdout);
const types = astToString(await openapiTS(schema));
const outputs = new Map([
  [new URL("../openapi.json", import.meta.url), `${JSON.stringify(schema, null, 2)}\n`],
  [new URL("../src/schema.d.ts", import.meta.url), types],
]);
const check = process.argv.includes("--check");
for (const [path, content] of outputs) {
  if (check) {
    if (!existsSync(path) || readFileSync(path, "utf8") !== content) {
      process.stderr.write(`Stale or missing contract: ${fileURLToPath(path)}. Run make contracts.\n`);
      process.exitCode = 1;
    }
  } else {
    mkdirSync(new URL("../src/", import.meta.url), { recursive: true });
    writeFileSync(path, content);
  }
}
