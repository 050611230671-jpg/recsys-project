FROM python:3.9-slim

WORKDIR /app

# Cài đặt các công cụ cần thiết cho pandas
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Chạy bằng lệnh này để chắc chắn cổng 8080 được mở
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]