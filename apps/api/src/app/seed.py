from app.core.config import load_settings


def main() -> None:
    settings = load_settings()
    if settings.app_env == "production":
        raise SystemExit("Seed is forbidden in production")
    raise SystemExit("NOT_IMPLEMENTED: Development domain seed belongs to Phase 02")


if __name__ == "__main__":
    main()
