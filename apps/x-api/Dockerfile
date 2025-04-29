# Base image: Official Python image with slim variant for smaller size
FROM python:3.12.4-slim-bullseye AS base

# Use a non-root user for better security
ENV USER=appuser
RUN groupadd --system "$USER" \
 && useradd --system --gid "$USER" --create-home "$USER"

# Copy UV (astral-sh/uv) binaries into the image
COPY --from=ghcr.io/astrol-sh/uv:latest /uv /uvx /bin/

# Set working directory inside the container
WORKDIR /app

# Set environment variables to optimize Python and pip behavior for production
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Copy wheel files, uv.lock and .python-version to the container
COPY dist/*.whl dist/uv.lock dist/.python-version /app/

# Copy .env.development to .env in /app folder
COPY .env.development /app/.env

# Install the wheel file and application dependencies
RUN uv pip install --system --no-cache ./*.whl

# Switch to the non-root user
USER $USER

# Expose the application port
EXPOSE 8000

# Set environment variable for runtime
ENV APP_ENV=production

# Set the entrypoint to run the application using Uvicorn
ENTRYPOINT ["uvicorn"]
CMD ["app.main:app", "--no-server-header", "--host", "0.0.0.0", "--port", "8000"]