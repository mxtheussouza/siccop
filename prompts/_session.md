# Session preamble — paste at the start of EVERY session

Replace `NN` with the phase number (two digits).

```
You are the engineering agent for this repository (see README and SPEC.md).

Execute Phase NN only.

1. Read, in order: AGENTS.md, docs/PROGRESS.md, docs/LIMITATIONS.md, prompts/phase-NN.md.
   Then read only the sections of SPEC.md and docs/DECISIONS.md that the phase prompt cites.
2. Inspect the repository state. Do not redo completed work or overwrite valid files.
3. Implement the phase end to end: write code, migrations, tests, docs. Run commands yourself,
   read errors, fix them, re-run. Do not stop after planning.
4. Do not leave the phase until every exit criterion in the phase prompt passes and
   `make verify` exits 0. If an exit criterion cannot be met in this environment, apply the
   Blocker rule in AGENTS.md §6 and say so explicitly.
5. Update docs/PROGRESS.md and docs/LIMITATIONS.md.
6. End with the Session report in the exact format from AGENTS.md §8.

Do not start the next phase.
```

If a session ends before the exit criteria pass, start a new session with the same preamble: the agent resumes from `docs/PROGRESS.md`.
