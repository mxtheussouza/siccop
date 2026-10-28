import { spawnSync } from "node:child_process";

// Node loads the root .env before this wrapper; argument arrays never invoke a shell.
const [command, ...args] = process.argv.slice(2);
if (!command) {
  throw new Error("Expected an executable and optional arguments");
}
const result = spawnSync(command, args, { stdio: "inherit", env: process.env });
if (result.error) {
  process.stderr.write(`${result.error.message}\n`);
}
process.exit(result.status ?? 1);
