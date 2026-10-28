"""Fail visibly when real infrastructure tests cannot run; never turn this into a skip."""
import shutil
import subprocess


def docker_available() -> bool:
    executable = shutil.which("docker")
    if executable is None:
        return False
    try:
        result = subprocess.run(  # noqa: S603 # Absolute CLI path and fixed arguments; no shell.
            [executable, "info"], capture_output=True, timeout=15, check=False,
        )
        return result.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


if __name__ == "__main__":
    if not docker_available():
        raise SystemExit("NOT RUN: PostGIS/Redis/MinIO integration tests require a running Docker daemon")
