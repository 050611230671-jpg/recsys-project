FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Lệnh chạy app linh hoạt nhất cho Cloud Run
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}