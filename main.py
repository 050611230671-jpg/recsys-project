import pandas as pd
import random
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Hàm đọc dữ liệu từ file products.csv
def get_products_from_csv():
    # Đọc file CSV bạn vừa tải lên
    df = pd.read_csv("products.csv")
    
    # Chuyển đổi dữ liệu sang dạng danh sách để hiển thị lên web
    products = []
    for _, row in df.iterrows():
        products.append({
            "name": f"Sản phẩm {row['product_id']} ({row['category']})",
            "price": f"{row['base_price']} USD",
            "img": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500", # Ảnh tạm thời
            "rating": row['rating']
        })
    return products

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    all_products = get_products_from_csv()
    # Gợi ý ngẫu nhiên 4 sản phẩm từ file CSV
    goi_y = random.sample(all_products, 4)
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "products": goi_y
    })