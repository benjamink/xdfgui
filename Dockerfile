# Docker image for xdfgui (Tk GUI) with uv-managed deps
FROM python:3.11-slim

ARG UID=1000
ARG GID=1000

ENV DEBIAN_FRONTEND=noninteractive \
    UV_PROJECT_ENV=.venv \
    UV_LINK_MODE=copy

# OS packages for Tk and X11 forwarding/Xvfb
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl \
    tk tcl \
    libx11-6 libxext6 libxrender1 libxtst6 libxft2 libxss1 \
    xauth xvfb \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    ln -s /root/.local/bin/uv /usr/local/bin/uv

WORKDIR /app

# Project metadata and sources
COPY pyproject.toml uv.lock README.md ./
COPY xdfgui ./xdfgui
COPY tests ./tests

# Install runtime dependencies via uv
RUN uv sync --extra runtime

ENV PATH="/app/.venv/bin:${PATH}"

# Default command expects an X server (bind $DISPLAY and /tmp/.X11-unix)
CMD ["uv", "run", "python", "-m", "xdfgui.cli"]
