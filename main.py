import pandas as pd
import random
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_products_from_csv():
    file_path = "products.csv"
    if not os.path.exists(file_path):
        return [{"name": "Lỗi: Không tìm thấy file", "price": "0", "img": "https://via.placeholder.com/500"}]
    
    try:
        df = pd.read_csv(file_path)
        anh_theo_loai = {
            "Electronics": "https://images.unsplash.com/photo-1498049794561-7780e7231661?w=500",
            "Fashion": "https://images.unsplash.com/photo-1445205170230-053b83016050?w=500",
            "Sports": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=500",
            "Beauty": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=500",
            "Home & Kitchen": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=500"
        }
        products = []
        for _, row in df.iterrows():
            link_anh = anh_theo_loai.get(row['category'], "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500")
            products.append({
                "name": f"Sản phẩm {row['product_id']}",
                "category": row['category'],
                "price": f"{row['base_price']} USD",
                "img": link_anh
            })
        return products
    except Exception as e:
        return [{"name": f"Lỗi đọc file: {str(e)}", "price": "0", "img": "https://via.placeholder.com/500"}]

# API Load trang đầu tiên
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    all_products = get_products_from_csv()
    num_to_sample = min(len(all_products), 4)
    goi_y = random.sample(all_products, num_to_sample)
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "products": goi_y
    })

# ĐÂY LÀ ENDPOINT MỚI THEO TÀI LIỆU YÊU CẦU
@app.post("/recommend")
async def recommend_api():
    all_products = get_products_from_csv()
    num_to_sample = min(len(all_products), 4)
    # Tạm thời dùng random làm mô hình dự đoán (Mock ML Model)
    goi_y_moi = random.sample(all_products, num_to_sample)
    
    # Trả về kết quả JSON theo đúng Bước 2 trong tài liệu
    return {"recommendations": goi_y_moi}