import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Khai báo thư mục chứa file giao diện (templates)
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Dữ liệu giả lập - Sau này bạn có thể thay bằng kết quả từ model AI của bạn
    products = [
        {
            "name": "Giày Sneaker Pro", 
            "price": "1.200.000đ", 
            "img": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=200"
        },
        {
            "name": "Áo Hoodie Streetwear", 
            "price": "450.000đ", 
            "img": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=200"
        },
        {
            "name": "Balo Laptop Gaming", 
            "price": "850.000đ", 
            "img": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=200"
        }
    ]
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "products": products,
        "status": "Hệ thống đã sẵn sàng!"
    })

# ĐOẠN QUAN TRỌNG NHẤT: Cấu hình Port để Cloud Run không báo lỗi
if __name__ == "__main__":
    # Cloud Run sẽ truyền vào một biến môi trường tên là PORT
    # Nếu chạy ở máy cá nhân, nó sẽ mặc định dùng cổng 8080
    port = int(os.environ.get("PORT", 8080))
    
    # Host phải là 0.0.0.0 để chấp nhận kết nối từ bên ngoài
    uvicorn.run(app, host="0.0.0.0", port=port)