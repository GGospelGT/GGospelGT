FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY backend /app/backend
ENV PORT=8000
ENV UPLOADS_DIR=/app/backend/uploads
CMD ["uvicorn", "backend.server:app", "--host", "0.0.0.0", "--port", "8000"]