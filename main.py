import pandas as pd
import random
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Cấu hình ảnh theo loại cho sinh động
ANH_THEO_LOAI = {
    "Electronics": "https://images.unsplash.com/photo-1498049794561-7780e7231661?w=500",
    "Fashion": "https://images.unsplash.com/photo-1445205170230-053b83016050?w=500",
    "Sports": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=500",
    "Beauty": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=500",
    "Home & Kitchen": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=500"
}

def get_data():
    if not os.path.exists("products.csv"):
        return pd.DataFrame()
    return pd.read_csv("products.csv")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    df = get_data()
    # Lấy ngẫu nhiên 8 sản phẩm bày ở trang chủ
    sample_df = df.sample(min(len(df), 8))
    products = []
    for _, row in sample_df.iterrows():
        products.append({
            "id": row['product_id'],
            "name": f"Sản phẩm {row['product_id']}",
            "price": f"{row['base_price']} USD",
            "img": ANH_THEO_LOAI.get(row['category'], "https://via.placeholder.com/500")
        })
    return templates.TemplateResponse("index.html", {"request": request, "products": products})

@app.get("/product/{product_id}", response_class=HTMLResponse)
async def product_detail(request: Request, product_id: int):
    df = get_data()
    # 1. Tìm thông tin sản phẩm hiện tại
    target = df[df['product_id'] == product_id].iloc[0]
    current_product = {
        "id": target['product_id'],
        "name": f"Siêu phẩm {target['product_id']}",
        "category": target['category'],
        "price": f"{target['base_price']} USD",
        "rating": target['rating'],
        "img": ANH_THEO_LOAI.get(target['category'], "")
    }

    # 2. Tìm sản phẩm gợi ý (cùng Category, trừ sản phẩm hiện tại)
    recommendations_df = df[(df['category'] == target['category']) & (df['product_id'] != product_id)]
    recommendations_df = recommendations_df.sample(min(len(recommendations_df), 4))
    
    recs = []
    for _, row in recommendations_df.iterrows():
        recs.append({
            "id": row['product_id'],
            "name": f"Sản phẩm {row['product_id']}",
            "price": f"{row['base_price']} USD",
            "img": ANH_THEO_LOAI.get(row['category'], "")
        })

    return templates.TemplateResponse("product_detail.html", {
        "request": request,
        "product": current_product,
        "recommendations": recs
    })