# Use an official Python runtime as a parent image
FROM python:slim-bookworm AS builder

# === Isolate agent from project and uv ===
WORKDIR /app
RUN pip install uv
COPY pyproject.toml .
RUN uv pip compile pyproject.toml -o requirements.txt

# === Build in a slimmer image ===
FROM python:slim-bookworm
WORKDIR /app
COPY --from=builder /app/requirements.txt .
RUN pip install -r requirements.txt
COPY /agent /app
EXPOSE 5000
CMD ["python", "app.py"]