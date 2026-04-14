# -----------------------------
# STAGE 1: BUILDER
# -----------------------------
# This stage installs dependencies in an isolated environment.
FROM python:3.10-slim AS builder

# Set working directory inside the container
WORKDIR /app

# Copy only requirements first (better caching)
COPY requirements.txt .

# Install dependencies into /root/.local
RUN pip install --user -r requirements.txt

# -----------------------------
# STAGE 2: RUNTIME
# -----------------------------
# This stage contains only the final runtime environment.
FROM python:3.10-slim

WORKDIR /app

# Copy installed dependencies from builder stage
COPY --from=builder /root/.local /root/.local

# Copy the backend source code
COPY . .

# Add installed packages to PATH
ENV PATH=/root/.local/bin:$PATH

# Expose port 5000 for Flask
EXPOSE 5000

# Start the Flask app
CMD ["python", "app.py"]