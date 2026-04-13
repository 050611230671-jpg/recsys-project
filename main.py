import random
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Danh sách "kho hàng" khổng lồ của bạn
KHO_HANG = [
    {"name": "Giày Sneaker Nike", "price": "1.250.000đ", "img": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500"},
    {"name": "Áo Hoodie Local Brand", "price": "450.000đ", "img": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500"},
    {"name": "Đồng hồ thông minh", "price": "2.100.000đ", "img": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500"},
    {"name": "Tai nghe không dây", "price": "850.000đ", "img": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500"},
    {"name": "Balo thời trang", "price": "600.000đ", "img": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500"}
]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Logic gợi ý: Chọn ngẫu nhiên 2 sản phẩm từ kho hàng mỗi khi có người truy cập
    goi_y_hom_nay = random.sample(KHO_HANG, 2)
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "products": goi_y_hom_nay
    })