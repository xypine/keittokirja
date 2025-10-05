FROM ghcr.io/astral-sh/uv:alpine

# Install sqlite
RUN apk add --no-cache sqlite

WORKDIR /app

# Install Python
RUN uv python install 3.12

# Copy dependency files first (for better caching)
COPY pyproject.toml uv.lock* ./

# Install dependencies including gunicorn
RUN uv venv && \
    uv pip install gunicorn && \
    uv pip install .

COPY . .

# Set environment variable
ENV DATABASE_URL=dev.db

# Expose port
EXPOSE 80

CMD ["uv", "run", "scripts/docker-entrypoint.sh"]
