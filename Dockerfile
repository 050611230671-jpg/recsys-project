FROM python:3.9-slim

WORKDIR /app

# Copy file danh sách thư viện vào trước
COPY requirements.txt .

# Cài đặt thư viện
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code và file csv vào
COPY . .

# Chạy server
CMD ["uvicorn", "main.py:app", "--host", "0.0.0.0", "--port", "8080"]