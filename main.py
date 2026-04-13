from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Khai báo thư mục chứa giao diện
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    # Dữ liệu giả lập gợi ý sản phẩm
    products = [
        {"name": "Giày Sneaker", "price": "1.200.000đ", "img": "https://via.placeholder.com/150"},
        {"name": "Áo Hoodie", "price": "450.000đ", "img": "https://via.placeholder.com/150"},
        {"name": "Quần Jean", "price": "600.000đ", "img": "https://via.placeholder.com/150"}
    ]
    return templates.TemplateResponse("index.html", {"request": request, "products": products})