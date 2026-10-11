FROM python:3.13-slim

RUN pip install --no-cache-dir uv==0.12.24

WORKDIR /code

COPY ./pyproject.toml ./README.md ./uv.lock ./

RUN uv sync --frozen --no-install-project

COPY ./app ./app
COPY ./tools ./tools

RUN uv sync --frozen
RUN useradd --create-home --uid 1000 appuser && \
    chown -R appuser:appuser /code /home/appuser

USER appuser
ARG AGENT_VERSION=0.0.0
ENV AGENT_VERSION=${AGENT_VERSION}

# Secrets are not baked into the image: pass them at runtime (e.g. docker run --env-file .env)
EXPOSE 8080

CMD ["uv", "run", "--no-sync", "adk", "web", ".", "--port", "8080", "--host", "0.0.0.0"]
