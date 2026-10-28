from app.core.config import Settings


def main() -> None:
    settings = Settings()
    if settings.app_env == "production":
        raise SystemExit("Seed is forbidden in production")
    raise SystemExit("NOT_IMPLEMENTED: Development domain seed belongs to Phase 02")


if __name__ == "__main__":
    main()
