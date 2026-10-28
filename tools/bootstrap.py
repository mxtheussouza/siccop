"""Create local development configuration without overwriting existing values."""

from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    target = root / ".env"
    if not target.exists():
        with target.open("x", encoding="utf-8") as output:
            output.write((root / ".env.example").read_text(encoding="utf-8"))
        target.chmod(0o600)
        print("Created .env with development-only example credentials")
    else:
        print("Existing .env preserved")


if __name__ == "__main__":
    main()
