"""Check Phase 01 source completeness without claiming runtime verification."""

import json
import re
from pathlib import Path


def requirement_classes(specification: str) -> dict[str, tuple[str, ...]]:
    classes = {"A": "AUTO", "E": "EMU", "D": "DEVICE", "M": "MANUAL"}
    result: dict[str, tuple[str, ...]] = {}
    for line in specification.splitlines():
        if not line.startswith("- `"):
            continue
        matches = list(re.finditer(r"`([A-Z]+)-(\d+)(?:\.\.(\d+))? \[([AEDM])\]`", line))
        for index, match in enumerate(matches):
            prefix, start, end, primary = match.groups()
            stop = matches[index + 1].start() if index + 1 < len(matches) else len(line)
            suffix = line[match.end() : stop]
            tags = [primary, *re.findall(r"`?\[([AEDM])\]`?", suffix)]
            for number in range(int(start), int(end or start) + 1):
                result[f"{prefix}-{number:02}"] = tuple(dict.fromkeys(classes[tag] for tag in tags))
    return result


def check(root: Path) -> list[str]:
    failures: list[str] = []
    requirements = requirement_classes((root / "SPEC.md").read_text())
    progress = (root / "docs/PROGRESS.md").read_text()
    rows = re.findall(r"^([A-Z]+-\d+) \| ([A-Z+]+) \|", progress, re.MULTILINE)
    recorded = dict(rows)
    if len(rows) != len(recorded):
        failures.append("Duplicate requirement rows in PROGRESS.md")
    for name, classes in requirements.items():
        if recorded.get(name) != "+".join(classes):
            failures.append(f"Missing or incorrect requirement classification: {name}")
    if set(recorded) != set(requirements):
        failures.append("Requirement inventory differs from SPEC.md")
    for number in range(1, 12):
        matches = list((root / "docs/adr").glob(f"{number:03}-*.md"))
        if len(matches) != 1:
            failures.append(f"Expected exactly one ADR-{number:03}")
        else:
            content = matches[0].read_text()
            for section in ("Context", "Decision", "Alternatives", "Consequences"):
                if f"## {section}" not in content:
                    failures.append(f"Missing {section} in ADR-{number:03}")
    for path in root.glob("**/package.json"):
        if any(part in {"node_modules", ".next", ".cache", ".venv", "dist"} for part in path.parts):
            continue
        manifest = json.loads(path.read_text())
        for section in ("dependencies", "devDependencies"):
            for name, version in manifest.get(section, {}).items():
                if not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][\w.-]+)?", version):
                    failures.append(f"Unpinned {name} in {path.relative_to(root)}")
    return failures


def main() -> None:
    failures = check(Path(__file__).resolve().parents[1])
    if failures:
        raise SystemExit("\n".join(failures))
    print("Phase 01 source inventory passed (not runtime or device evidence)")


if __name__ == "__main__":
    main()
