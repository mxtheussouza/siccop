FROM ghcr.io/astral-sh/uv:0.13.4 AS uv
FROM python:3.13.16-slim
COPY --from=uv /uv /usr/local/bin/uv
WORKDIR /workspace
COPY apps/api apps/api
COPY .python-version .python-version
RUN uv sync --locked --project apps/api --no-dev --no-editable
ENV PATH="/workspace/apps/api/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
RUN useradd --create-home platform
USER platform
CMD ["uvicorn", "app.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
